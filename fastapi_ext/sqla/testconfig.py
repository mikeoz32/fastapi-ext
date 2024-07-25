
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Mapping, cast
from fastapi import FastAPI
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.sql.elements import True_

from fastapi_ext.sqla.di import get_main_async_session
from fastapi_ext.sqla.engine import create_engine
from fastapi_ext.sqla.lifespan import migrate
from fastapi_ext.sqla.model import M
from fastapi_ext.sqla.settings import sqla_settings


ModelMapping = Mapping[str, M]

@pytest_asyncio.fixture(scope="session")
async def test_database():
    uri = sqla_settings.database_uri
    @asynccontextmanager
    async def _test_database():
        # engine = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost:5432/", echo=True)
        # async with engine.begin() as conn:
        #     await conn.execute("CREATE DATABASE `bd`")
        yield uri

    return _test_database

@pytest_asyncio.fixture(scope="session")
async def main_engine(test_database):
    async with test_database() as url:
        engine = create_engine(str(url))
        await migrate(engine)

        yield engine

        await engine.dispose()


@pytest_asyncio.fixture
async def main_session(main_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    connection = await main_engine.connect()
    transaction = await connection.begin()

    session = AsyncSession(
        bind=connection,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    yield session

    session.expunge_all()
    await transaction.rollback()
    await connection.close()

@pytest.fixture(autouse=True)
def sqla_dependency_overrides(dependency_overrides, main_session):
    print("Overriding!")
    dependency_overrides[get_main_async_session] = lambda: main_session


@pytest.fixture
def data_mapping() -> Dict[str, ModelMapping]:
    return dict()

@pytest_asyncio.fixture
async def test_data(main_engine, data_mapping: Dict[str, ModelMapping]):
    async with main_engine.begin() as connection:
        async with AsyncSession(bind=connection, expire_on_commit=False) as session:
            for model in data_mapping.values():
                for object in cast(ModelMapping, model).values():
                    session.add(object)
            await session.commit()

            for model in data_mapping.values():
                for object in cast(ModelMapping, model).values():
                    await session.refresh(object)
            yield data_mapping

class TestConfig():

    def setup_dependency_overrides(self, app: FastAPI):
        print("Setting up overrides")
        app.dependency_overrides[get_main_async_session] = lambda: main_session()

config = TestConfig()
