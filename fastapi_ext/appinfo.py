import importlib
import os

from fastapi_ext.settings import settings


class Lifespan:
    def __init__(self, mod) -> None:
        self._mod = mod

    @property
    def init(self):
        return self.get("init")

    @property
    def dispose(self):
        return self.get("dispose")

    @property
    def init_app(self):
        return self.get("init_app")

    def get(self, name: str):
        if self._mod and hasattr(self._mod, name):
            return getattr(self._mod, name)
        return None


class AppInfo:
    def __init__(self, path: str) -> None:
        mod = importlib.import_module(path)
        self._mod = mod

        self.name = mod.__name__
        self.dir = os.path.dirname(mod.__file__)
        self.path = path

    def _import(self, path: str):
        parts = path.split(".")
        mod = self._mod
        try:
            for part in parts:
                mod = getattr(mod, part)
        except Exception:
            return None

        return mod

    @property
    def lifespan(self):
        return Lifespan(self._import("lifespan"))

    @property
    def router(self):
        return self._import("routes.router")

    @property
    def app(self):
        return self._import("app")

    @property
    def test_config(self):
        if hasattr(self._mod, "testconfig"):
            return f"{self.path}.testconfig"
        return None

    @property
    def cli(self):
        return self._import("cli.app")

    def __repr__(self) -> str:
        return f"AppInfo(router={self.router}, lifespan={self.lifespan}, dir={self.dir}, test={self.test_config})"


def load_apps():
    apps = [AppInfo(app) for app in settings.apps]
    return apps
