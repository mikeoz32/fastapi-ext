from typing import Callable, Dict, Optional, TypedDict

from fastapi import FastAPI


class Lifespan(TypedDict):
    init: Callable[..., TypedDict]
    dispose: Optional[Callable[..., None]] = None


class LifespanManager:
    def __init__(self) -> None:
        self._hooks: Dict[str, Lifespan] = dict()

    def add_lifespan(
        self,
        name: str,
        init: Callable[..., TypedDict],
        dispose: Optional[Callable[..., None]],
    ):
        self._hooks[name] = Lifespan(init=init, dispose=dispose)

    async def init(self, app: FastAPI) -> TypedDict:
        result = dict()
        for name, span in self._hooks.items():
            result[name] = await span["init"]()
        return result

    async def dispose(self, state: TypedDict):
        for name, span in self._hooks.items():
            await span["dispose"](state[name])


lifespan_manager = LifespanManager()

__all__ = ["lifespan_manager"]
