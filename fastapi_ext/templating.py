
from typing import List, Optional
from fastapi import Request
from fastapi.templating import Jinja2Templates

from jinja2 import ChoiceLoader, Environment, PackageLoader, PrefixLoader

from fastapi_ext.appinfo import AppInfo

templates:Optional[Jinja2Templates] = None

def init_apps(apps: List[AppInfo]):
    prefixes = dict()
    for app in apps:
        prefixes[app.name] = ChoiceLoader([PackageLoader(app.path)])

    return Jinja2Templates(env=Environment(loader=PrefixLoader(prefixes), extensions=['jinja2.ext.debug']))


def templates_init(apps: List[AppInfo]):
    async def hook():
        return init_apps(apps)
    return hook

async def get_templates(request: Request):
    return request.state.templates

__all__ = ["templates_init", "get_templates"]
