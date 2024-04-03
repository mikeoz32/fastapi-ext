from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_main_async_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    assert (
        "main_async_session_maker" in request.state
    ), "No session maker, please provide main_async_session_maker as state property in lifespan"

    async with request.state.main_async_session_maker() as session:
        yield session
