import inquirer
import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from what_to_eat.gateways import wolt
from what_to_eat.models.wolt import Item, Restaurant


def select_restaurant(items: list[Item]) -> Restaurant:
    questions = [
        inquirer.List(
            "restaurant",
            message="Several restaurants found, can you specify which one exactly?",
            choices=[item.title for item in items],
        ),
    ]
    answer = inquirer.prompt(questions)

    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        progress.add_task(description="Loading...", total=None)
        return wolt.restaurant(next(item for item in items if item.title == answer["restaurant"]))


def confirm_overwrite() -> None:
    if not inquirer.confirm("Config file already exists, overwrite?"):
        raise typer.Exit(0)


def get_profile_name(default: str = "Default") -> str:
    return inquirer.text("Profile name", default=default)


def get_address(default: str = "Kraków") -> str:
    return inquirer.text("Your address", default=default)
