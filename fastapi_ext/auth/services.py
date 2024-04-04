from typing import Annotated

from fastapi import Depends
from fastapi_ext.auth.password import hash_password

from fastapi_ext.auth.repositories import IdentityRepository

class IdentityAlreadyExistsException(Exception):
    ...

class AuthenticationService:
    def __init__(self, identities: Annotated[IdentityRepository, Depends()]) -> None:
        self.identities = identities

    async def create_identity(self, *, email: str, password: str):
        existing = await self.identities.get_by_email(email=email)
        if existing:
            raise IdentityAlreadyExistsException()
        password_hash = hash_password(password)

        entity = self.identities.create(email=email, password_hash=password_hash)
        entity = await self.identities.save(entity)
        
        return entity
