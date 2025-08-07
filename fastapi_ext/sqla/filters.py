from typing import Protocol, Any
from sqlalchemy.sql import Select
from sqlalchemy.orm import DeclarativeBase


class Filter(Protocol):
    def apply(self, stmt: Select, model: type[DeclarativeBase]) -> Select: ...

class Equal:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def apply(self, stmt: Select, model: type) -> Select:
        return stmt.where(getattr(model, self.field) == self.value)


class In:
    def __init__(self, field: str, values: list[Any]):
        self.field = field
        self.values = values

    def apply(self, stmt: Select, model: type) -> Select:
        return stmt.where(getattr(model, self.field).in_(self.values))


class Like:
    def __init__(self, field: str, pattern: str):
        self.field = field
        self.pattern = pattern

    def apply(self, stmt: Select, model: type) -> Select:
        return stmt.where(getattr(model, self.field).like(self.pattern))


class NotEqual:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def apply(self, stmt: Select, model: type) -> Select:
        return stmt.where(getattr(model, self.field) != self.value)


class GreaterThan:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def apply(self, stmt: Select, model: type) -> Select:
        return stmt.where(getattr(model, self.field) > self.value)


class LessThan:
    def __init__(self, field: str, value: Any):
        self.field = field
        self.value = value

    def apply(self, stmt: Select, model: type) -> Select:
        return stmt.where(getattr(model, self.field) < self.value)
