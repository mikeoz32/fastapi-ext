from typing import Annotated, Any, Optional, Protocol, TypeVar
from typing_extensions import Doc
from fastapi import Request
from dataclasses import Field, dataclass
from uuid import UUID, uuid4

from jose import jwt

ST = TypeVar("ST")


class SessionStorage(Protocol[ST]):
    ...


@dataclass
class SessionId:
    session_id: UUID = Field(default_factory=uuid4)


class JWSSigner:
    def sign(self, session_id: SessionId):
        return jwt.encode(session_id.__dict__, "secret", algorithm="HS256")


class Session:
    def __init__(
        self,
        *,
        cookie_name: Annotated[Optional[str], Doc("")] = None,
        cookie_auto_create: Annotated[
            Optional[bool], Doc("Initialize cookie without data")
        ] = None,
    ) -> None:
        self._cookie_name = cookie_name or "session_cookie_name"
        self._cookie_auto_create = cookie_auto_create or True

    async def __call__(self, request: Request) -> Any:
        signature = request.cookies.get(self._cookie_name)

        if signature is None:
            return self 

        return self
