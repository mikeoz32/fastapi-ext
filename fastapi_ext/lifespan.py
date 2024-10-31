from typing import Callable, Dict, Optional, TypedDict, Any

from fastapi import FastAPI

from fastapi_ext.appinfo import AppInfo


class Lifespan(TypedDict):
    init: Callable[..., Dict]
    dispose: Optional[Callable[[], None]]


class LifespanManager:
    def __init__(self) -> None:
        self._hooks: Dict[str, Lifespan] = dict()

    def add_lifespan(
        self,
        name: str,
        init: Callable[..., Any],
        dispose: Optional[Callable[..., Any]] = None,
    ):
        self._hooks[name] = Lifespan(init=init, dispose=dispose)

    async def init(self, app: FastAPI) -> Dict:
        result = dict()
        for name, span in self._hooks.items():
            result[name] = await span["init"](app)  # type: ignore
        return result

    async def dispose(self, state: Dict):
        for name, span in self._hooks.items():
            if span["dispose"] is not None:
                await span["dispose"](state[name])  # type: ignore

    def add_app_info(self, info: AppInfo):
        if info.lifespan.init:
            dispose = info.lifespan.dispose
            self.add_lifespan(info.name, info.lifespan.init, dispose)


lifespan_manager = LifespanManager()

__all__ = ["lifespan_manager"]
