import contextlib
from typing import Annotated, Optional
from typing_extensions import Doc
from fastapi import FastAPI
from fastapi_ext.settings import settings
from fastapi_ext.lifespan import lifespan_manager
from fastapi_ext.sqla.lifespan import sqla_dispose, sqla_init

import importlib


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    state = await lifespan_manager.init(app)
    print(state)
    yield state
    await lifespan_manager.dispose(state)


class AppInfo:
    def __init__(self, path: str) -> None:
        mod = importlib.import_module(path)

        self.name = mod.__name__

        try:
            self.router = mod.routes.router
        except Exception:
            self.router = None

    def __repr__(self) -> str:
        return f"AppInfo(router={self.router})"

def load_app(app: str) -> AppInfo:
    info = AppInfo(app)
    print(info)
    return info

def create_app(
    debug: Annotated[bool, Doc("")] = False, title: Annotated[Optional[str], Doc("")] = None
) -> FastAPI:
    if debug is False:
        debug = settings.debug

    title = title or settings.title

    sqla = settings.sqla



    if sqla is not None:
        lifespan_manager.add_lifespan("sqla", sqla_init, sqla_dispose)


    app = FastAPI(debug=debug, lifespan=lifespan)
    for path in settings.apps:
        info = load_app(path)
        if info.router:
            app.include_router(router=info.router, prefix=f"/{info.name}")
    return app


__all__ = ["create_app"]
