from typing import Annotated
from aiopenid.integrations.fastapi import OAuth2AuthorizationCodeCallback
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from fastapi_ext.auth.repositories import AccountRepository
from fastapi_ext.auth.di import client


router = APIRouter()


oauth_callback = OAuth2AuthorizationCodeCallback(client)


@router.get("/oauth-callback", name="oauth-callback")
async def oauth_callback(
    request: Request,
    accounts: Annotated[AccountRepository, Depends()] = None,
    token=Depends(oauth_callback),
):
    token_info = client.decode_token(token["access_token"])
    email = token_info.get("email")
    id = token_info.get("sub")
    await accounts.create_if_not_exists(id, email)
    response = RedirectResponse(url=f"{request.base_url}app")
    response.set_cookie(key="token", value=token["access_token"])
    return response


@router.get("/")
async def authenticate(request: Request):
    return RedirectResponse(
        url=client.get_authorization_url(redirect_url=request.url_for("oauth-callback"))
    )
