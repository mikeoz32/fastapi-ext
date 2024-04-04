

import importlib


class AppInfo:
    def __init__(self, path: str) -> None:
        mod = importlib.import_module(path)

        self.name = mod.__name__
        self.path = path

        try:
            self.router = mod.routes.router
        except Exception:
            self.router = None

    def __repr__(self) -> str:
        return f"AppInfo(router={self.router})"
