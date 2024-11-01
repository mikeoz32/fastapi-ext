from typing import Protocol, TypeVar
from uuid import UUID, uuid4

from fastapi import Request, Response
from jose import jwt
from pydantic import BaseModel, Field

from fastapi_ext.logger import logger

ST = TypeVar("ST")


class SessionStorage(Protocol[ST]): ...


class InMemorySessionStorage:
    def __init__(self) -> None:
        self._session_data = dict()

    async def save(self, session_id, data):
        self._session_data[session_id] = data

    async def get(self, session_id):
        return self._session_data.get(session_id)


class SessionId(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)


class JWSSigner:
    def sign(self, session_id: SessionId):
        return jwt.encode(session_id.__dict__, "secret", algorithm="HS256")


# class Session:
#     def __init__(
#         self,
#         *,
#         name: Annotated[str, Doc("")],
#         auto_create: Annotated[
#             Optional[bool], Doc("Initialize cookie without data")
#         ] = None,
#     ) -> None:
#         self._name = name
#         self._auto_create = auto_create or True
#         self._storage = InMemorySessionStorage()
#         self._session_id = None
#
#     async def __call__(self, request: Request, response: Response) -> Any:
#         signature = request.cookies.get(self._name)
#
#         if signature is None:
#             session_id = SessionId()
#             signature = jwt.encode(jsonable_encoder(session_id.model_dump()), "secret", algorithm="HS256")
#             response.set_cookie(key=self._name, value=signature, domain="http://localhost:8000", samesite=None)
#             print(signature)
#             await self._storage.save(session_id.session_id, {})
#
#         data = jwt.decode(signature, "secret", algorithms=["HS256"])
#         self.session_id = data.get('session_id')
#
#         return self
#
#     async def data(self):
#         return self._storage.get(self.session_id)


class Session:
    def __init__(self, *, name: str, id: UUID) -> None:
        self.name = name
        self.id = id
        self._modified = False
        self._data = dict()

    def modified(self):
        return self._modified

    def __repr__(self) -> str:
        return f"Session(name={self.name}, id={self.id}, modified={self._modified}, data={self._data})"

    def __getitem__(self, key):
        return self._data.get(key)

    def __setitem__(self, key, val):
        self._modified = True
        self._data[key] = val

    def get(self, key):
        return self._data.get(key)

    def keys(self):
        return self._data.keys()


class SessionManager:
    def __init__(self) -> None:
        self._sessions = dict()
        self._storage = InMemorySessionStorage()

    async def get_session(self, *, session_name: str, request: Request):
        session = await self.get_session_from_request(
            session_name=session_name, request=request
        )

        if session is None:
            session = Session(name=session_name, id=uuid4())
            await self._storage.save(str(session.id), session)

        logger.info(f"Session ID {session.id}")
        self._sessions[session_name] = session
        return session

    async def get_session_from_request(self, *, session_name: str, request: Request):
        signature = request.cookies.get(session_name)

        if signature is None:
            return None

        data = None
        try:
            data = jwt.decode(signature, "secret")
        except Exception as e:
            logger.error(e)
            return None

        session_id = data.get("session_id")

        if session_id is None:
            return None

        session = await self._storage.get(session_id)

        return session

    async def flush(self, response: Response):
        for name, session in self._sessions.items():
            if session.modified():
                await self._storage.save(str(session.id), session)
            signature = jwt.encode(
                dict(session_id=str(session.id)), "secret", algorithm="HS256"
            )
            response.set_cookie(name, signature)
