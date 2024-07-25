from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable, Dict, Mapping
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
import httpx
import asgi_lifespan
import pytest_asyncio
import pytest

from fastapi_ext.appinfo import load_apps
from fastapi_ext.sqla.model import M


ModelMapping = Mapping[str, M]

HTTPClientGeneratorType = Callable[
    [FastAPI], AbstractAsyncContextManager[httpx.AsyncClient]
]

apps = load_apps()
pytest_plugins = [app.test_config for app in apps if app.test_config is not None]

@pytest.fixture(scope="session", autouse=True)
def apps():
    apps = load_apps()
    [app.test_config for app in apps]
    return apps

@pytest.fixture(scope="session", autouse=True)
def dependency_overrides():
    overrides = dict()
    return overrides

def data_mapping() -> Dict:
    ...

@pytest_asyncio.fixture
async def test_data(main_engine, data_mapping):
    async with main_engine.begin() as connection:
        async with AsyncSession(bind=connection, expire_on_commit=False) as session:
            for model in data_mapping.values():
                for object in cast(ModelMapping, model).values():
                    session.add(object)
            await session.commit()

            for model in data_mapping.values():
                for object in cast(ModelMapping, model).values():
                    await session.refresh(object)

@pytest_asyncio.fixture
async def test_client_generator(apps, dependency_overrides) -> HTTPClientGeneratorType:
    @asynccontextmanager
    async def _test_client_generator(app: FastAPI):
        app.dependency_overrides = dependency_overrides

        async with asgi_lifespan.LifespanManager(app):
            async with httpx.AsyncClient(
                app=app, base_url="https://test.app"
            ) as client:
                yield client

    return _test_client_generator
