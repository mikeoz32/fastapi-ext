from typing import TypedDict
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_ext.settings import settings

from fastapi_ext.sqla.engine import create_engine


class SqlaLifespan(TypedDict):
    engine: AsyncEngine


def create_main_engine() -> AsyncEngine:
    assert settings.sqla, "Sql Alchemy is not enabled, please enable it in config"
    return create_engine(settings.sqla.database_uri)


async def sqla_init() -> SqlaLifespan:
    return SqlaLifespan(engine=create_main_engine())


async def sqla_dispose(lifespan: SqlaLifespan):
    engine = lifespan["engine"]
    await engine.dispose()
