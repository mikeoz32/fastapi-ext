from typing import Annotated, TypedDict
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_ext.sqla.model import Base, CreatedUpdatedAtMixin, IDMixin
from fastapi_ext.sqla.schema import AutoSchemaMixin

"""
# Authentication module

## Identity

An identity to authenticate (think user or profile) have only data related to
authentication, like email, username, password_hash/salt and links to OpenID identities
"""

class Identity(IDMixin, CreatedUpdatedAtMixin, AutoSchemaMixin, Base):
    __tablename__ = "identity"

    email: Mapped[Annotated[str, mapped_column(index=True, unique=True)]]
    password_hash: Mapped[str]
    email_verified: Mapped[Annotated[bool, mapped_column(default=False)]]
    is_active: Mapped[Annotated[bool, mapped_column(default=True)]]
