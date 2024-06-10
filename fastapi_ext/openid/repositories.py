
from typing import Optional

from fastapi_ext.openid.models import AuthorizationCode, Identity
from fastapi_ext.sqla.repository import (
    BaseRepository,
    SelectOptions,
    UIDRepositoryMixin,
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


class AuthorizationCodeRepository(UIDRepositoryMixin, BaseRepository[AuthorizationCode]):
    model = AuthorizationCode
