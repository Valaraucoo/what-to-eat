import typer
from rich import print
from rich.console import Console

from wte.gateways import wolt
from wte.models import Ordering, Sort
from wte.models.config import Profile
from wte.models.wolt import Item
from wte.services import filters
from wte.services.display import build_items_table, build_restaurant_table


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
    items = filters.filter_by_name(items, restaurant)

    if len(items) == 0:
        print(f"[red]Restaurant [cyan italic]{restaurant}[/][red] not found[/red]")
        raise typer.Exit()
    if len(items) > 1:
        print(
            f"[red]More than one restaurant found for [cyan italic]{restaurant}[/][red]. "
            f"Try to specify one restaurant[/red]"
        )
        raise typer.Exit()

    restaurant = wolt.restaurant(items[0].link)

    table = build_restaurant_table(restaurant=restaurant)

    console = Console()
    console.print(table)
