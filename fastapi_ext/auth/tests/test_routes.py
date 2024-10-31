import pytest
import pytest_asyncio
from fastapi_ext.auth import app
from fastapi_ext.pytest.plugin import HTTPClientGeneratorType
import httpx

@pytest_asyncio.fixture
async def client(test_client_generator: HTTPClientGeneratorType) -> httpx.AsyncClient:
    async with test_client_generator(app) as client:
        yield client


@pytest.mark.asyncio
async def test_authenticate(client: httpx.AsyncClient, test_data):
    response = await client.get("/check")
    print(test_data)
    assert response.json() == 200
