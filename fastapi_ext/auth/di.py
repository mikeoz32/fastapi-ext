from typing import Annotated, Any, Dict
from aiopenid.oauth2 import OpenID

from aiopenid.integrations.fastapi import OAuth2AuthorizationCodeBearer
from fastapi import Depends, HTTPException, status
from fastapi_ext.auth.repositories import AccountRepository
from fastapi_ext.auth.settings import auth_settings


client = OpenID(
    client_id=auth_settings.client_id,
    client_secret=auth_settings.client_secret,
    openid_configuration_endpoint=auth_settings.openid_configuration_endpoint,
)

oauth_scheme = OAuth2AuthorizationCodeBearer(client=client)


async def get_token_info(
    token: Annotated[OAuth2AuthorizationCodeBearer, Depends(oauth_scheme)],
):
    try:
        return client.decode_token(token)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


async def get_account(
    token_info: Annotated[Dict[str, Any], Depends(get_token_info)],
    accounts: Annotated[AccountRepository, Depends()],
):
    account = await accounts.get_by_itentity_id(token_info["sub"])
    if not account:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return account


async def get_or_create_account(
    token_info: Annotated[Dict[str, Any], Depends(get_token_info)],
    accounts: Annotated[AccountRepository, Depends()],
):
    account = await accounts.create_if_not_exists(
        token_info["sub"], token_info["email"]
    )

    return account


__all__ = [
    "client",
    "oauth_scheme",
    "get_token_info",
    "get_account",
    "get_or_create_account",
]
