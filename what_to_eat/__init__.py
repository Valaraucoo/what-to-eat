from importlib import metadata

import typer
from rich import print

__version__ = metadata.version(__package__)


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()
