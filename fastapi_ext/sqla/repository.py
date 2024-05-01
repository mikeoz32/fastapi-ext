from collections.abc import Sequence
from typing import Annotated, Any, Dict, Generic, List, Optional, Protocol, Union, cast
from typing_extensions import Doc
from uuid import UUID

from fastapi import Depends
from sqlalchemy import Result, Select, func, over, select
from sqlalchemy.orm import joinedload

from fastapi_ext.sqla.model import M, M_ID, M_UID
from fastapi_ext.sqla.entity_manager import AsyncEntityManager


SelectOptions = Optional[Sequence[Any]]


class BaseRepositoryProtocol(Protocol[M]):
    model: type[M]
    manager: AsyncEntityManager

    async def all(self, options: SelectOptions = None) -> list[M]: ...

    async def list(self, statement: Select) -> list[M]: ...

    async def get_one_or_none(self, statement: Select) -> Union[M, None]: ...

    def create(self, **kwargs) -> M: ...

    async def delete(self, model: M): ...

    async def save(self, entity: M) -> M: ...


def apply_options(statement: Select, options: Optional[Sequence[Any]] = None) -> Select:
    if options is not None:
        statement = statement.options(*options)
    return statement


class QueryBuilder(Generic[M]):
    def __init__(self, entity_type: type[M], fields: List[str] = []) -> None:
        self.entity_type = entity_type
        if len(fields) > 0:
            self.statement = select(*[self._get_field(x) for x in fields])
        else:
            self.statement = select(entity_type)

    def limit(self, limit: Annotated[Optional[int], Doc("")] = None):
        if limit:
            self.statement = self.statement.limit(limit)
        return self

    def offset(self, offset: Annotated[Optional[int], Doc("")] = None):
        if offset:
            self.statement = self.statement.offset(offset)
        return self

    def where(self, where: Annotated[Optional[dict], Doc("")] = None):
        if where:
            for name, value in where.items():
                attr = self._get_field(name)
                self.statement = self.statement.where(attr == value)
        return self

    def _get_field(self, name: str):
        if not hasattr(self.entity_type, name):
            raise Exception(f"Unknown field name {name}")
        return getattr(self.entity_type, name)

    def build(self):
        return self.statement


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

    async def delete(self, model: M):
        return await self.entity_manager.delete(model)

    async def find(
        self,
        limit: Annotated[Optional[int], Doc("")] = None,
        offset: Annotated[Optional[int], Doc("")] = None,
        where: Annotated[Optional[Dict[str, Any]], Doc("")] = None,
        options: SelectOptions = None,
    ):
        builder = QueryBuilder(self.model).limit(limit).offset(offset).where(where)

        statement = builder.build()
        statement = apply_options(statement, options)

        return await self.list(statement)

    async def find_one(
        self,
        where: Annotated[Optional[Dict[str, Any]], Doc("")] = None,
        options: SelectOptions = None,
    ):
        builder = QueryBuilder(self.model).where(where)
        statement = builder.build()
        statement = apply_options(statement, options)

        return await self.get_one_or_none(statement)

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


class IDRepositoryProtocol(BaseRepositoryProtocol, Protocol[M_ID]):
    async def get_by_id(
        self, id: int, options: SelectOptions = None
    ) -> Union[M_ID, None]: ...


class IDRrepositoryMixin(Generic[M_ID]):
    async def get_by_id(
        self: IDRepositoryProtocol, id: int, options: SelectOptions = None
    ):
        statement = select(self.model).where(self.model.id == id)
        statement = apply_options(statement, options)

        return await self.get_one_or_none(statement)


class UIDRepositoryProtocol(BaseRepositoryProtocol, Protocol[M_ID]):
    async def get_by_id(
        self, id: UUID, options: Optional[SelectOptions] = None
    ) -> Union[M_ID, None]: ...


class UIDRepositoryMixin(Generic[M_UID]):
    async def get_by_id(
        self: UIDRepositoryProtocol, id: UUID, options: Optional[SelectOptions] = None
    ):
        statement = select(self.model).where(self.model.id == id)
        statement = apply_options(statement, options)

        return await self.get_one_or_none(statement)
