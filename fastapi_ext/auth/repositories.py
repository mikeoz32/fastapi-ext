from fastapi_ext.sqla.repository import BaseRepository
from sqlalchemy import select

from fastapi_ext.auth.models import Account

class AccountRepository(BaseRepository[Account]):
    model = Account

    async def create_if_not_exists(self, identity_id: str, email: str):
        statement = select(Account).where(Account.identity_id == identity_id)
        account = await self.get_one_or_none(statement)
        if not account:
            account = self.create(identity_id = identity_id, name = email)
            account = await self.save(account)
        return account

    async def  get_by_itentity_id(self, identity_id: str):
        statement = select(Account).where(Account.identity_id == identity_id)
        return await self.get_one_or_none(statement)
