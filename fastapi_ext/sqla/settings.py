from typing import Literal
from pydantic_core import MultiHostUrl

from fastapi_ext.settings import Settings


class SqlaSettings(Settings):
    database_uri: MultiHostUrl = "sqlite+aiosqlite://"
    init_tables: Literal["drop_create", "none", "migrate"] = "none"


sqla_settings = SqlaSettings()
