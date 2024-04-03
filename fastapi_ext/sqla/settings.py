from pydantic import BaseModel
from pydantic_core import MultiHostUrl


class SqlaSettings(BaseModel):
    database_uri: MultiHostUrl = "sqlite+aiosqlite://"

