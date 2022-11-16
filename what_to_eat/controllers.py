import random

import typer
from rich import print
from rich.console import Console

from what_to_eat.gateways import wolt
from what_to_eat.models import Ordering, Sort
from what_to_eat.models.config import Profile
from what_to_eat.models.wolt import Item
from what_to_eat.services import filters
from what_to_eat.services.display import build_items_table, build_restaurant_table
from what_to_eat.services.weights import EvaluateTechnique, build_weights
from what_to_eat.utils.prompt import select_restaurant


def items_controller(
    items: list[Item],
    profile: Profile,
    query: str | None,
    tag: str | None,
    sort: Sort,
    ordering: Ordering,
    limit: int | None,
) -> None:
    if query:
        items = filters.filter_by_query(items, query)
    if tag:
        items = filters.filter_by_tag(items, tag)
    if sort:
        items = filters.sort_by(items, sort, ordering)
    if limit:
        items = items[:limit]

    if not items:
        print("[red]No restaurants found")
        raise typer.Exit(0)

    table = build_items_table(items=items)
    table.caption = f":popcorn: Restaurants in [italic bold cyan]{profile.address}[/] via wolt :popcorn:"

    console = Console()
    console.print(table)


def restaurant_controller(items: list[Item], restaurant: str) -> None:
    items = filters.filter_by_title(items, restaurant)

    if not items:
        print(f"[red]Restaurant [cyan italic]{restaurant}[/][red] not found[/red]")
        raise typer.Exit()

    if len(items) > 1:
        restaurant = select_restaurant(items)  # type: ignore[assignment]
    else:
        restaurant = wolt.restaurant(items[0])  # type: ignore[assignment]

    table = build_restaurant_table(restaurant)  # type: ignore[arg-type]

    console = Console()
    console.print(table)


def random_controller(items: list[Item], tag: str | None, technique: EvaluateTechnique) -> None:
    if tag:
        items = filters.filter_by_tag(items, tag)

    if not items:
        print("[red]No restaurants found")
        raise typer.Exit(0)

    item = random.choices(population=items, weights=build_weights(items, technique), k=1)[0]
    restaurant = wolt.restaurant(item)

    table = build_restaurant_table(restaurant=restaurant)

    console = Console()
    console.print(table)
