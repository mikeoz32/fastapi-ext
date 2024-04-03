from example.models.base import BaseModel

from fastapi_ext.sqla.model import IDMixin, CreatedUpdatedAtMixin, TimestamableMixin


class User(IDMixin, CreatedUpdatedAtMixin, TimestamableMixin, BaseModel):
    __tablename__ = "users"
