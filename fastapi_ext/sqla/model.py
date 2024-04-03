from datetime import datetime, timezone
from typing import Annotated, TypeVar
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

UTC = timezone.utc


def now_utc():
    return datetime.now(UTC)

class BaseModel:
    ...


class IDMixin(BaseModel):
    id: Mapped[Annotated[int, mapped_column(primary_key=True, autoincrement=True)]]


class CreatedAtMixin(BaseModel):
    created_at: Mapped[
        Annotated[
            datetime,
            mapped_column(
                TIMESTAMP(timezone=True),
                server_default=func.now(),
                index=True,
                default=now_utc,
            ),
        ]
    ]


class UpdatedAtMixin(BaseModel):
    updated_at: Mapped[
        Annotated[
            datetime,
            mapped_column(
                TIMESTAMP(timezone=True),
                server_default=func.now(),
                index=True,
                default=now_utc,
                onupdate=now_utc,
            ),
        ]
    ]


class CreatedUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin):
    ...


class TimestamableMixin(BaseModel):
    timestamp: Mapped[Annotated[datetime, mapped_column(TIMESTAMP(timezone=False))]]


M = TypeVar("M", bound=DeclarativeBase)
M_ID = TypeVar("M_ID", bound=IDMixin)
M_TS = TypeVar("M_TS", bound=TimestamableMixin)

__all__ = [
    "IDMixin",
    "CreatedAtMixin",
    "UpdatedAtMixin",
    "CreatedUpdatedAtMixin",
    "TimestamableMixin",
    "M",
    "M_ID",
    "M_TS",
]
