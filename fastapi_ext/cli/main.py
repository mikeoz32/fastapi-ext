import os
import sys
from typing import Any
from fastapi_ext.cli import typer

from fastapi_ext.appinfo import load_apps

app = typer.Typer()

sys.path.append(os.getcwd())

apps = load_apps()

for info in apps:
    cli = info.cli
    if cli:
        print(cli)
        app.add_typer(cli, name=info.name)

if __name__ == "__main__":
    app()
