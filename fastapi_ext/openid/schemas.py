
from typing import Annotated, Literal, Optional, Union
from fastapi import Depends, HTTPException, status
from pydantic import AnyUrl, BaseModel, EmailStr, Field
from fastapi_ext.openid.models import Identity


IdentitySchema = Identity.schema()
CreateIdentitySchema = Identity.create_model_schema()
UpdateIdentitySchema = Identity.update_model_schema()


class RegisterIdentity(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class AuthorizeRequest(BaseModel):
    email: EmailStr
    password: str


class OAuth2AuthorizaRequest:
    def __init__(
        self,
        response_type: Literal["code"],
        client_id: str,
        redirect_uri: Optional[AnyUrl],
        scope: Optional[str] = None,
        state: Optional[str] = None,
    ) -> None:
        if response_type != "code":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        if client_id != "account":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.response_type = response_type
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.state = state


class AuthorizationCodeGrant:
    def __init__(
        self,
        grant_type: str,
        code: Optional[str] = None,
        redirect_uri: Optional[AnyUrl] = None,
    ) -> None:
        if grant_type != "authorization_code":
            return
        self.grant_type = grant_type

        self.code = code
        self.redirect_uri = redirect_uri


class PasswordGrant:
    def __init__(
        self,
        grant_type: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        redirect_uri: Optional[AnyUrl] = None,
    ) -> None:
        if grant_type != "password":
            return

        self.grant_type = grant_type

        if not password or not username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        self.username = username
        self.password = password


class OAuth2TokenRequest:
    def __init__(
        self,
        grant_type: Union[Literal["authorization_code"], Literal["password"]],
        code_grant: Annotated[AuthorizationCodeGrant, Depends()],
        password_grant: Annotated[PasswordGrant, Depends()]
    ) -> None:
        if grant_type == "authorization_code":
            self.grant = code_grant
        elif grant_type == "password":
            self.grant = password_grant
