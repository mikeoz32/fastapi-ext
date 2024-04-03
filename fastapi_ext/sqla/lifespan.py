from typing import Any, TypedDict
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_ext.settings import settings

from fastapi_ext.sqla.engine import create_async_session_maker, create_engine


class SqlaLifespan(TypedDict):
    engine: AsyncEngine
    main_async_session_maker: Any


def create_main_engine() -> AsyncEngine:
    assert settings.sqla, "Sql Alchemy is not enabled, please enable it in config"
    return create_engine(settings.sqla.database_uri)


def create_main_async_session_maker(engine: AsyncEngine):
    return create_async_session_maker(engine)

async def sqla_init() -> SqlaLifespan:
    engine = create_main_engine()
    session_maker = create_main_async_session_maker(engine)
    return SqlaLifespan(engine=create_main_engine(), main_async_session_maker=session_maker)


async def sqla_dispose(lifespan: SqlaLifespan):
    engine = lifespan["engine"]
    await engine.dispose()
