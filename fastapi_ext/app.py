import contextlib
from typing import Annotated, Optional
from typing_extensions import Doc
from fastapi import FastAPI
from fastapi_ext.appinfo import AppInfo
from fastapi_ext.settings import settings
from fastapi_ext.lifespan import lifespan_manager
from fastapi_ext.sqla.lifespan import sqla_dispose, sqla_init

from fastapi_ext.templating import templates_init


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    state = await lifespan_manager.init(app)
    print(state)
    yield state
    await lifespan_manager.dispose(state)



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

    apps = [load_app(app) for app in settings.apps]

    for info in apps:
        if info.lifespan and hasattr(info.lifespan, 'init'):
            dispose = None
            if hasattr(info.lifespan, 'dispose'):
                dispose = info.lifespan.dispose
            lifespan_manager.add_lifespan(info.name, info.lifespan.init, dispose)

    lifespan_manager.add_lifespan("templates", templates_init(apps))

    if sqla is not None:
        lifespan_manager.add_lifespan("sqla", sqla_init, sqla_dispose)


    app = FastAPI(debug=debug, lifespan=lifespan)

    for info in apps:
        if info.lifespan and hasattr(info.lifespan, 'init_app'):
            info.lifespan.init_app(app)
        if info.router:
            app.include_router(router=info.router, prefix=f"/{info.name}")
    return app


__all__ = ["create_app", "AppInfo"]
