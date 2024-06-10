from typing import Literal
from fastapi_ext.settings import Settings


class OpenIDSettings(Settings):
    secret_key: str = "change_this_secret"
    algorithm: Literal["HS256"] = "HS256"
    access_token_expire: int = 30
    auth_session_name: str = "auth_session"


openid_settings = OpenIDSettings()
