from typing import Annotated

from fastapi import Depends

from fastapi_ext.auth.repositories import IdentityRepository


class AuthenticationService:
    def __init__(self, identities: Annotated[IdentityRepository, Depends()]) -> None:
        pass

    async def create_identity(self):
        return {"id":10}
