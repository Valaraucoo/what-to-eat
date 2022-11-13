from typing import Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from wte.services.profile import find_profile
from wte.models import Ordering, Sort
from wte import config, controllers, validators
from wte.gateways import wolt

app = typer.Typer(no_args_is_help=True)


@app.command()
def ls(
    restaurant: Optional[str] = typer.Argument(    # noqa: U007
        default=None,
        help="Restaurant name",
        callback=validators.validate_restaurant,
    ),
    query: Optional[str] = typer.Option(    # noqa: U007
        None,
        "--query",
        "-q",
        help="Query search for restaurants",
        callback=validators.validate_query,
    ),
    profile_name: Optional[str] = typer.Option(None, "--profile", "-p", help="Profile name"),    # noqa: U007
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag"),    # noqa: U007
    sort: Sort = typer.Option(
        Sort.NONE,
        "--sort",
        "-s",
        help=f"Sort by: {', '.join(Sort.choices())}",
        case_sensitive=False,
    ),
    ordering: Ordering = typer.Option(
        Ordering.ASC,
        "--ordering",
        "-o",
        help=f"Ordering: {', '.join(Ordering.choices())}",
        case_sensitive=False
    ),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit results"),    # noqa: U007
) -> None:
    """Finds best restaurants via Wolt API"""
    profile = find_profile(profile_name)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Fetching data...", total=None)
        items = wolt.items(location=profile.location)

    if restaurant:
        return controllers.restaurant_controller(items, restaurant)
    return controllers.items_controller(items, profile, query, tag, sort, ordering, limit)


@app.command()
def random(
    profile_name: Optional[str] = typer.Option(None, "--profile", "-p", help="Profile name"),    # noqa: U007
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag"),    # noqa: U007
) -> None:
    """Finds random restaurant via Wolt API"""
    # TODO: add more options
    profile = find_profile(profile_name)
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Fetching data...", total=None)
        items = wolt.items(location=profile.location)

    controllers.random_controller(items, tag)


@app.command()
def configure() -> None:
    """Create configuration file to your orders"""
    config.manage()
