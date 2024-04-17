import importlib
import os

from fastapi_ext.settings import settings


class AppInfo:
    def __init__(self, path: str) -> None:
        mod = importlib.import_module(path)

        self.name = mod.__name__
        self.dir = os.path.dirname(mod.__file__)
        self.path = path

        try:
            self.router = mod.routes.router
        except Exception:
            self.router = None

        try:
            self.lifespan = mod.lifespan
        except Exception:
            self.lifespan = None

    @property
    def cli(self):
        try:
            return mod.cli.app
        except:
            return None

    def __repr__(self) -> str:
        return f"AppInfo(router={self.router}, lifespan={self.lifespan}, dir={self.dir})"


def load_apps():
    apps = [AppInfo(app) for app in settings.apps]
    print(apps)
    return apps
