import contextlib
from typing import Annotated, Optional
from typing_extensions import Doc
from fastapi import FastAPI
from fastapi_ext.appinfo import AppInfo, load_apps
from fastapi_ext.settings import settings
from fastapi_ext.lifespan import lifespan_manager
from fastapi_ext.logger import init_logger, logger

from fastapi_ext.templating import templates_init


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    init_logger()
    state = await lifespan_manager.init(app)
    logger.debug(state)
    logger.info(f"{app.title} services are started")
    yield state
    await lifespan_manager.dispose(state)
    logger.info(f"{app.title} services are stopped")


def create_app(
    debug: Annotated[bool, Doc("")] = False,
    title: Annotated[Optional[str], Doc("")] = None,
) -> FastAPI:
    if debug is False:
        debug = settings.debug

    title = title or settings.title

    apps = load_apps()

    for info in apps:
        lifespan_manager.add_app_info(info)

    lifespan_manager.add_lifespan("templates", templates_init(apps))

    app = FastAPI(lifespan=lifespan, debug=debug, title="Fastapi Ext application")

    for info in apps:
        if info.lifespan.init_app:
            info.lifespan.init_app(app)

        if info.app:
            app.mount(f"/{info.name}", info.app)
    return app


__all__ = ["create_app", "AppInfo"]
