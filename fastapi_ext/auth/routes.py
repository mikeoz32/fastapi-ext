from typing import Annotated, Any, List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr, Field, ValidationError
from fastapi_ext.auth.schemas import (
    AuthorizeRequest,
    CreateIdentitySchema,
    IdentitySchema,
    RegisterIdentity,
)

from fastapi_ext.auth.services import (
    AuthenticationService,
    IdentityAlreadyExistsException,
    IdentityBadCredentialsException,
)
from fastapi_ext.auth.token import get_identity_claims, jwt_encode
from fastapi_ext.forms import FormBase, FormValidationException
from fastapi_ext.templating import get_templates

router = APIRouter()


@router.post("/token")
async def get_auth_token(
    request: AuthorizeRequest, service: Annotated[AuthenticationService, Depends()]
):
    try:
        identity = await service.authorize(
            email=request.email, password=request.password
        )
    except IdentityBadCredentialsException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    token = jwt_encode(get_identity_claims(identity))
    return token


@router.post("/register")
async def create_identity(
    identity: RegisterIdentity, service: Annotated[AuthenticationService, Depends()]
):
    try:
        return await service.create_identity(
            email=identity.email, password=identity.password
        )
    except IdentityAlreadyExistsException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


class LoginForm(FormBase):
    email: EmailStr
    password: str = Field(..., min_length=1)


@router.get("/login")
async def login(
    request: Request, templates: Annotated[Jinja2Templates, Depends(get_templates)]
):
    response = templates.TemplateResponse(request, "auth/login.html")
    return response


@router.post("/login")
async def post_login(
    request: Request,
    templates: Annotated[Jinja2Templates, Depends(get_templates)],
    service: Annotated[AuthenticationService, Depends()],
):
    scope = dict()
    form = await LoginForm.validate_request(request)
    if form.is_valid():
        try:
            identity = await service.authorize(email=form.email, password=form.password)
        except IdentityBadCredentialsException as e:
            scope['auth_error'] = str(e)

    scope["form"] = form
    print(form.is_valid())
    print(form.errors())

    response = templates.TemplateResponse(request, "auth/login.html", context=scope)
    return response


@router.get("/logout")
async def logout():
    ...


@router.get("/identities", response_model=List[IdentitySchema])
async def list_identities():
    ...
