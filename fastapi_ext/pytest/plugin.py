from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Callable
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI
import httpx
import asgi_lifespan
import pytest_asyncio
import pytest

from fastapi_ext.appinfo import load_apps


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
