from typing import Literal
from fastapi_ext.settings import Settings

class AuthSettings(Settings):
    secret_key: str = "change_this_secret"
    algorithm: Literal["HS256"] = "HS256"
    access_token_expire: int = 30

auth_settings = AuthSettings()
