from collections.abc import Sequence
from typing import Annotated, Any, Generic, List, Optional, Union, cast

from fastapi import Depends
from sqlalchemy import Result, Select, func, over, select
from sqlalchemy.orm import joinedload

from fastapi_ext.sqla.model import M
from fastapi_ext.sqla.entity_manager import AsyncEntityManager


SelectOptions = Optional[Sequence[Any]]


def apply_options(statement: Select, options: Optional[Sequence[Any]] = None) -> Select:
    if options is not None:
        statement = statement.options(*options)
    return statement


class BaseRepository(Generic[M]):
    model: type[M]

    def __init__(self, manager: Annotated[AsyncEntityManager, Depends()]) -> None:
        self.manager = manager

    async def all(self, options: SelectOptions = None) -> list[M]:
        return await self.list(apply_options(select(self.model), options))

    async def list(self, statement: Select) -> list[M]:
        result = await self._execute_query(statement)
        return cast(list[M], result.scalars().unique().all())

    async def get_one_or_none(self, statement: Select) -> Union[M, None]:
        return await self.manager.get_one_or_none(statement)

    def create(self, **kwargs) -> M:
        return self.model(**kwargs)

    # async def find(
    #     self,
    #     find_options: ListQuery,
    #     statement: Optional[Select] = None,
    #     unique=False,
    #     expand: List[str] = [],
    # ):
    #     if statement is None:
    #         fields = find_options.fields
    #         if fields is None:
    #             statement = select(self.model)
    #         else:
    #             statement = select(*[getattr(self.model, attr) for attr in fields])
    #
    #     statement = statement.limit(find_options.top).offset(find_options.skip)
    #     if len(expand) > 0:
    #         statement = statement.options(
    #             joinedload(*[getattr(self.model, x) for x in expand])
    #         )
    #     statement = statement.add_columns(over(func.count()))
    #
    #     results: list[M] = []
    #     count: int = 0
    #
    #     rows = await self._execute_query(statement)
    #
    #     if unique is True:
    #         rows = rows.unique()
    #
    #     for row in rows:
    #         if len(row) == 2:
    #             results.append(row[0])
    #             count = row[1]
    #         else:
    #             results.append(row[:-1])
    #             count = row[-1]
    #
    #     return results, count

    async def save(self, entity: M) -> M:
        return await self.manager.save(entity)

    async def _execute_query(self, query: Select) -> Result:
        return await self.manager.execute_query(query)
