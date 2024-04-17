import asyncio
from asyncio import iscoroutine
import functools
import inspect
from typing import Any, Callable, Dict, Optional, Type, Union
import typer
from typer.core import TyperCommand
from typer.models import CommandFunctionType, CommandInfo
import asyncclick as click


def async_command(f: Callable[..., Any]):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(f(*args, **kwargs))
        loop.close()
    return wrapper

class Typer(typer.Typer):
    def command(self, name: Optional[str] = None,
                *, 
                cls: Optional[Type[TyperCommand]] = None,
                context_settings: Optional[Dict[Any, Any]] = None, 
                help: Optional[str] = None, 
                epilog: Optional[str] = None, 
                short_help: Optional[str] = None, 
                options_metavar: str = "[OPTIONS]", 
                add_help_option: bool = True,
                no_args_is_help: bool = False,
                hidden: bool = False, 
                deprecated: bool = False, 
                rich_help_panel: Union[str, None] = ...) -> Callable[[CommandFunctionType], CommandFunctionType]:

        if cls is None:
            cls = TyperCommand

        def decorator(f: CommandFunctionType) -> CommandFunctionType:
            if inspect.iscoroutinefunction(f):
                f = async_command(f)
            self.registered_commands.append(
                CommandInfo(
                    name=name,
                    cls=cls,
                    context_settings=context_settings,
                    callback=f,
                    help=help,
                    epilog=epilog,
                    short_help=short_help,
                    options_metavar=options_metavar,
                    add_help_option=add_help_option,
                    no_args_is_help=no_args_is_help,
                    hidden=hidden,
                    deprecated=deprecated,
                    # Rich settings
                    rich_help_panel=rich_help_panel,
                )
            )
            return f

        return decorator


