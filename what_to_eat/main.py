from typing import Optional

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from what_to_eat import config, controllers, version_callback
from what_to_eat.gateways import wolt
from what_to_eat.gateways.location import LocationError
from what_to_eat.gateways.wolt import WoltApiError
from what_to_eat.models import Ordering, Sort
from what_to_eat.services.profile import find_profile
from what_to_eat.services.weights import EvaluateTechnique
from what_to_eat.utils import handle, validators

app = typer.Typer(no_args_is_help=True)


@app.callback()
def common(_: bool = typer.Option(None, "--version", "-v", callback=version_callback)):
    pass


@app.command()
@handle.exception(WoltApiError)
def ls(
    restaurant: Optional[str] = typer.Argument(  # noqa: U007
        default=None,
        help="Restaurant name",
        callback=validators.validate_restaurant,
    ),
    query: Optional[str] = typer.Option(  # noqa: U007
        None,
        "--query",
        "-q",
        help="Query search for restaurants",
        callback=validators.validate_query,
    ),
    profile_name: Optional[str] = typer.Option(None, "--profile", "-p", help="Profile name"),  # noqa: U007
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag"),  # noqa: U007
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
        case_sensitive=False,
    ),
    limit: Optional[int] = typer.Option(None, "--limit", "-l", help="Limit results"),  # noqa: U007
) -> None:
    """List restaurants queried from Wolt API."""
    profile = find_profile(profile_name)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching data...", total=None)
        items = wolt.items(location=profile.location)

    if restaurant:
        return controllers.restaurant_controller(items, restaurant)
    return controllers.items_controller(items, profile, query, tag, sort, ordering, limit)


@app.command()
@handle.exception(WoltApiError)
def random(
    profile_name: Optional[str] = typer.Option(None, "--profile", "-p", help="Profile name"),  # noqa: U007
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Tag"),  # noqa: U007
    technique: EvaluateTechnique = typer.Option(
        EvaluateTechnique.MIX,
        help=f"Technique: {', '.join(EvaluateTechnique.choices())}",
        case_sensitive=False,
    ),
) -> None:
    """Finds random restaurant via Wolt API"""
    profile = find_profile(profile_name)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Fetching data...", total=None)
        items = wolt.items(location=profile.location)

    controllers.random_controller(items, tag, technique)


@app.command()
@handle.exception(LocationError)
def configure() -> None:
    """Create configuration file to your orders"""
    config.manage()
