from fastapi.applications import FastAPI
from fastapi_ext.auth import routes

__name__ = "auth"

app = FastAPI()

app.include_router(routes.router)

__all__ = ["app"]
