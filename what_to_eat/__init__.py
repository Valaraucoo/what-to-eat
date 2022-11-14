from typing import Final
from rich import print

import typer

VERSION: Final[str] = "0.1.2"


def version_callback(value: bool):
    if value:
        print(VERSION)
        raise typer.Exit()
