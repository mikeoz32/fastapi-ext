from typing import Annotated

from fastapi import Depends, Request, Response
from fastapi_ext.auth.models import Identity
from fastapi_ext.auth.password import hash_password, verify_password 

from fastapi_ext.auth.repositories import IdentityRepository

class IdentityAlreadyExistsException(Exception):
    def __init__(self, email: str) -> None:
        self.email = email

    def __repr__(self) -> str:
        return f"Identity with email {self.email} already exists"

    def __str__(self) -> str:
        return self.__repr__()

class IdentityBadCredentialsException(Exception):
    def __repr__(self) -> str:
        return "Bad credentials, could not find identity by email or bad password"

    def __str__(self) -> str:
        return self.__repr__()

class AuthenticationService:
    def __init__(self, identities: Annotated[IdentityRepository, Depends()]) -> None:
        self.identities = identities

    async def create_identity(self, *, email: str, password: str):
        existing = await self.identities.get_by_email(email=email)
        if existing:
            raise IdentityAlreadyExistsException(email=email)
        password_hash = hash_password(password=password)

        entity = self.identities.create(email=email, password_hash=password_hash)
        entity = await self.identities.save(entity)
        
        return entity

    async def authorize(self, *, email: str, password: str) -> Identity:
        existing = await self.identities.get_by_email(email=email)
        if existing is None:
            raise IdentityBadCredentialsException()
        if not verify_password(password=password, hash=existing.password_hash):
            raise IdentityBadCredentialsException()
        return existing


class AuthSessionService:
    def __init__(self, request: Request) -> None:
        pass
