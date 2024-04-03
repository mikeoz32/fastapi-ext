from typing import AsyncGenerator
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession


async def get_main_async_session(
    request: Request,
) -> AsyncGenerator[AsyncSession, None]:
    sqla = request.state.sqla
    assert (
        'main_async_session_maker' in sqla.keys()
    ), "No session maker, please provide main_async_session_maker as state property in lifespan"
    session_maker = sqla.get('main_async_session_maker')

    async with session_maker() as session:
        yield session
