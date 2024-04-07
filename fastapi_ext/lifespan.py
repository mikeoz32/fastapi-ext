from typing import Callable, Dict, Optional, TypedDict, Any

from fastapi import FastAPI


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
            result[name] = await span["init"]() # type: ignore
        return result

    async def dispose(self, state: Dict):
        for name, span in self._hooks.items():
            if span["dispose"] is not None:
                await span["dispose"](state[name]) # type: ignore


lifespan_manager = LifespanManager()

__all__ = ["lifespan_manager"]
