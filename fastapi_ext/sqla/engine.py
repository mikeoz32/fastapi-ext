from pydantic import validate_call
from pydantic_core import MultiHostUrl
from sqlalchemy import Engine, create_engine as ce
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker


@validate_call
def create_engine(database_url: MultiHostUrl) -> AsyncEngine:
    return create_async_engine(
        str(database_url), echo=False, use_insertmanyvalues=False
    )


def create_sync_engine(database_url: MultiHostUrl) -> Engine:
    return ce(str(database_url), echo=True)


def create_async_session_maker(engine: AsyncEngine):
    return async_sessionmaker(engine, expire_on_commit=False)


__all__ = ["create_engine", "create_async_session_maker"]
