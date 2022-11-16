from functools import wraps
from typing import Callable, TypeVar

import typer
from rich import print

T = TypeVar("T")


def exception(expected_exception: type[Exception], exit_code: int = 1) -> Callable[..., T]:
    def decorator(func: Callable[..., T]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except expected_exception as e:
                print(f"[red u]{e}[/]")
            except Exception as e:
                if isinstance(e, typer.Exit):
                    raise e
                print("[red u]💥 Unexpected error[/]")
            finally:
                raise typer.Exit(code=exit_code)

        return wrapper

    return decorator
