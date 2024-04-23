import functools
from typing import Annotated, Any, Awaitable, Callable, Optional

import alembic
from alembic.script import ScriptDirectory
from typer import Option
from fastapi_ext.appinfo import load_apps
from fastapi_ext.cli import typer
import asyncio
from alembic import command, config
import os

app = typer.Typer()

cfg = config.Config(os.path.dirname(__file__) + '/alembic.ini')
cfg.set_main_option('script_location', os.path.dirname(__file__))

cfg.set_main_option('version_path_separator', ':')

apps = load_apps()

locations = [f"{info.dir}/versions" for info in apps]
 

# print(":".join(locations))
cfg.set_main_option('version_locations', ":".join(locations))
cfg.set_main_option('file_template', "%%(epoch)s_%%(rev)s_%%(slug)s")

script = ScriptDirectory.from_config(cfg)

def get_head(branch: str):
    for head in script.revision_map.heads:
        if branch in  script.get_revision(head).branch_labels:
            return head
    return None


@app.command()
def info():
    for head in script.revision_map.heads:
        print(script.get_revision(head).branch_labels)
    # command.heads(cfg)

@app.command(name="generate")
async def generate(app_name: str):
    app_info = [info for info in apps if info.name == app_name]
    if len(app_info) == 0:
        raise Exception("Bad app name")
    app_info = app_info[0]
    head = get_head(app_info.name)
    # print(head)
    if head:
        command.revision(cfg, head=f"{app_info.name}@head")
    else:
        command.revision(cfg, head=f"base", branch_label=app_info.name, version_path=f"{app_info.dir}/versions")
    # command.revision(cfg, version_path=f"{app_info.dir}/versions")

@app.command(name="upgrade")
def upgrade():
    command.upgrade(cfg, "heads")
