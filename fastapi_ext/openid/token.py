from datetime import datetime, timedelta, timezone
from typing import List, Optional, Union
from jose import jwt
from pydantic import BaseModel, Field
from fastapi_ext.openid.models import Identity

from fastapi_ext.openid.settings import openid_settings

class JwtClaims(BaseModel):
    sub: str
    aud: Union[str, List[str]]
    exp: Optional[datetime] = None
    iat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

def get_expire():
    minutes = openid_settings.access_token_expire
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)

def jwt_encode(data: JwtClaims) -> str:
    secret_key = openid_settings.secret_key
    algorithm = openid_settings.algorithm

    if data.exp is None:
        data.exp = get_expire()

    encoded = jwt.encode(data.model_dump(), secret_key, algorithm=algorithm)

    return encoded

def jwt_decode(token:str):
    secret_key = openid_settings.secret_key
    algorithm = openid_settings.algorithm

    return jwt.decode(token, secret_key, algorithms=[algorithm])

def get_identity_claims(identity: Identity):
    return JwtClaims(sub=str(identity.id), aud="fastapi")
