import contextlib
from typing import Annotated, Optional
from typing_extensions import Doc
from fastapi import FastAPI
from fastapi_ext.settings import settings
from fastapi_ext.lifespan import lifespan_manager
from fastapi_ext.sqla.lifespan import sqla_dispose, sqla_init


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    state = await lifespan_manager.init(app)
    yield state
    await lifespan_manager.dispose(state)

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
    return app


__all__ = ["create_app"]
