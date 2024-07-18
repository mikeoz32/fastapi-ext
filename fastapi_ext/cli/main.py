from typing import Any
from fastapi_ext.cli import typer

from fastapi_ext.appinfo import load_apps
import fastapi_ext.sqla.cli

app = typer.Typer()

app.add_typer(fastapi_ext.sqla.cli.app, name="sqla")

apps = load_apps()

for info in apps:
    cli = info.cli
    if cli:
        print(cli)
        app.add_typer(cli, name=info.name)

if __name__ == "__main__":
    app()
