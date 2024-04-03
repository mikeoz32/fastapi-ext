from typing import Annotated

from fastapi import Depends

from fastapi_ext.auth.repositories import IdentityRepository


class AuthenticationService:
    def __init__(self, identities: Annotated[IdentityRepository, Depends()]) -> None:
        self.identities = identities

    async def create_identity(self, *, email: str, password: str):
        return {"id":10}
