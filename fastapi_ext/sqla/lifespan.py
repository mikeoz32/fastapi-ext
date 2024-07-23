from typing import Any, TypedDict
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi_ext.sqla.model import Base
from fastapi_ext.sqla.settings import sqla_settings
from fastapi_ext.sqla.engine import create_async_session_maker, create_engine


class SqlaLifespan(TypedDict):
    engine: AsyncEngine
    main_async_session_maker: Any


def create_main_engine() -> AsyncEngine:
    return create_engine(sqla_settings.database_uri)


def create_main_async_session_maker(engine: AsyncEngine):
    return create_async_session_maker(engine)

async def migrate(engine: AsyncEngine):
    if sqla_settings.init_tables == "drop_create":
        async with engine.begin() as c:
            await c.run_sync(Base.metadata.drop_all)
            await c.run_sync(Base.metadata.create_all)

async def init(app: FastAPI) -> SqlaLifespan:
    engine = create_main_engine()
    await migrate(engine)
    session_maker = create_main_async_session_maker(engine)
    print("Sqla lifespan initialized")
    return SqlaLifespan(engine=create_main_engine(), main_async_session_maker=session_maker)


async def dispose(lifespan: SqlaLifespan):
    engine = lifespan["engine"]
    await engine.dispose()
