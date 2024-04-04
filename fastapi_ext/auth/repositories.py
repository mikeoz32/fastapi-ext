

from typing import Optional

from sqlalchemy import select
from fastapi_ext.auth.models import Identity
from fastapi_ext.sqla.repository import BaseRepository


class IdentityRepository(BaseRepository[Identity]):
    model = Identity

    async def get_by_email(self, *, email: str) -> Optional[Identity]:
        statement = select(Identity).where(Identity.email == email)

        return await self.get_one_or_none(statement)
