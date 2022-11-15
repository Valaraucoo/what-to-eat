from importlib import metadata
from rich import print

import typer

__version__ = metadata.version(__package__)


def version_callback(value: bool):
    if value:
        print(__version__)
        raise typer.Exit()
