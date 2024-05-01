from typing import Optional

from sqlalchemy import select
from fastapi_ext.auth.models import AuthSession, Identity
from fastapi_ext.sqla.repository import (
    BaseRepository,
    SelectOptions,
    UIDRepositoryMixin,
    apply_options,
)


class IdentityRepository(BaseRepository[Identity]):
    model = Identity

    async def get_by_email(
        self, *, email: str, options: SelectOptions = None
    ) -> Optional[Identity]:
        # statement = select(Identity).where(Identity.email == email)
        # statement = apply_options(statement, options)
        #
        # return await self.get_one_or_none(statement)
        return await self.find_one(where=dict(email=email), options=options)


class AuthSessionRepository(UIDRepositoryMixin, BaseRepository[AuthSession]):
    model = AuthSession
