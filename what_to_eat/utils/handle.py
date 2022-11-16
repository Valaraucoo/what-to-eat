from functools import wraps
from typing import Callable, TypeVar

import typer
from rich import print

T = TypeVar("T")


def exception(ex: type[Exception], exit_code: int = 1) -> Callable[..., T]:
    def decorator(func: Callable[..., T]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except ex as e:
                print(f"[red u]{e}[/]")
                raise typer.Exit(code=exit_code)
            except Exception:
                print("[red u]💥 Unexpected error[/]")
                raise typer.Exit(code=exit_code)

        return wrapper

    return decorator
