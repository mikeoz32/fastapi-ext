from typing import Literal
from pydantic import BaseModel
from pydantic_core import MultiHostUrl


class SqlaSettings(BaseModel):
    database_uri: MultiHostUrl = "sqlite+aiosqlite://"
    init_tables: Literal["drop_create","none"] = "none"

