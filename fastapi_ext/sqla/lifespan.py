from typing import Any, TypedDict
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi_ext.logger import logger
from fastapi_ext.sqla.cli import cfg
from fastapi_ext.sqla.model import Base
from fastapi_ext.sqla.settings import sqla_settings
from fastapi_ext.sqla.engine import (
    create_async_session_maker,
    create_engine,
)

from alembic import command


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
    elif sqla_settings.init_tables == "migrate":

        def __execute_upgrade(conn):
            try:
                cfg.attributes["connection"] = conn
                command.upgrade(cfg, "heads")
            except Exception as e:
                logger.error(e)

        async with engine.begin() as c:
            try:
                await c.run_sync(__execute_upgrade)
            except Exception as e:
                logger.error(e)


async def init(app: FastAPI) -> SqlaLifespan:
    engine = create_main_engine()
    await migrate(engine)
    session_maker = create_main_async_session_maker(engine)
    logger.info("Sqla lifespan initialized")
    return SqlaLifespan(
        engine=create_main_engine(), main_async_session_maker=session_maker
    )


async def dispose(lifespan: SqlaLifespan):
    engine = lifespan["engine"]
    await engine.dispose()
