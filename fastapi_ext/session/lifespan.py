from typing import Any, TypedDict

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from fastapi_ext.logger import logger
from fastapi_ext.session.session import SessionManager



class SessionLifespan(TypedDict):
    manager: Any


class SessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        await request.state.session["manager"].flush(response)
        return response


def init_app(app: FastAPI):
    app.add_middleware(SessionMiddleware)


async def init(app: FastAPI):
    logger.info("initializing session manager")
    return SessionLifespan(manager=SessionManager())


async def dispose(state: SessionLifespan): ...
