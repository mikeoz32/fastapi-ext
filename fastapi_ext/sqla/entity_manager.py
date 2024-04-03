from typing import Annotated, TypeVar, Union
from fastapi import Depends
from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from fastapi_ext.sqla.di import get_main_async_session


DB = TypeVar("DB", bound=DeclarativeBase)


class AsyncEntityManager:
    def __init__(
        self, session: Annotated[AsyncSession, Depends(get_main_async_session)]
    ) -> None:
        self.session = session

    async def execute_query(self, statement: Select) -> Result:
        return await self.session.execute(statement)

    async def get_one_or_none(self, statement: Select) -> Union[DB, None]:
        result = await self.execute_query(statement)
        return result.unique().scalar_one_or_none()

    async def delete(self, entity):
        self.session.delete(entity)
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def save(self, entity):
        self.session.add(entity)
        try:
            await self.session.commit()
            await self.session.refresh(entity)
            return entity
        except Exception as e:
            await self.session.rollback()
            raise e


__all__ = ["AsyncEntityManager"]
