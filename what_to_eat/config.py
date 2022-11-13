from functools import lru_cache
from pathlib import Path
from typing import Final

import inquirer
import typer
from rich import print
from pydantic import ValidationError

from what_to_eat.gateways import location
from what_to_eat.models.config import Config, Profile
from what_to_eat.models.location import Location

default_config_path: Final[str] = ".what-to-eat-config.json"
config_file: Final[Path] = Path(default_config_path)


@lru_cache
def load() -> Config:
    if not config_file.is_file():
        print("[red]💥 Config file not found, run [italic]what-to-eat configure[/italic] first")
        raise typer.Exit(1)

    try:
        config = Config.parse_raw(config_file.read_text())
    except ValidationError as e:
        print(f"[red]💥 Config file is invalid: {e}")
        raise typer.Exit(1)

    return config


def manage() -> None:
    questions = [
        inquirer.List(
            "action",
            message="What do you want to do?",
            choices=[
                "Create new configuration",
                "Add profile",
                "List profiles",
                "Edit profile",
                "Set profile as default",
                "Remove profile"
            ],
        ),
    ]

    answers = inquirer.prompt(questions)
    action = answers["action"]

    match action:
        case "Create new configuration":
            _create()
        case "Add profile":
            _add()
        case "List profiles":
            _list()
        case "Edit profile":
            _edit()
        case "Set profile as default":
            _set_default()
        case "Remove profile":
            _remove()


def _create() -> Config:
    if config_file.is_file():
        _confirm_overwrite()

    profile_name = _get_profile_name()
    address = _get_address()
    detailed_location = _get_detailed_location(address)

    config = Config(
        profiles=[
            Profile(name=profile_name, is_default=True, address=address, location=detailed_location)
        ]
    )

    config_file.write_bytes(config.json().encode())

    print("[green]🏁 Config was created successfully!")
    return config


def _add() -> Config:
    config = load()

    profile_name = _get_profile_name()
    if profile_name in (p.name for p in config.profiles):
        print("[red]💥 Profile with this name already exists")
        raise typer.Exit(1)

    address = _get_address()
    detailed_location = _get_detailed_location(address)

    config.profiles.append(
        Profile(name=profile_name, address=address, location=detailed_location)
    )

    config_file.write_bytes(config.json().encode())

    print("[green]🏁 Profile was added successfully!")
    return config


def _edit() -> Config:
    config = load()

    profile = inquirer.list_input(
        "Which profile do you want to edit?",
        choices=[p.name for p in config.profiles],
    )

    profile = next(filter(lambda p: p.name == profile, config.profiles))

    profile.name = _get_profile_name(profile.name)
    profile.address = _get_address(profile.address)
    profile.location = _get_detailed_location(profile.address)

    config_file.write_bytes(config.json().encode())

    print("[green]🏁 Profile was updated successfully!")
    return config


def _list() -> None:
    config = load()
    for profile in config.profiles:
        print(profile)


def _set_default() -> Config:
    config = load()

    profile = inquirer.list_input(
        "Which profile do you want to set as default?",
        choices=[p.name for p in config.profiles],
    )

    for p in config.profiles:
        p.is_default = p.name == profile

    config_file.write_bytes(config.json().encode())

    print("[green]🏁 Profile was updated successfully!")
    return config


def _remove() -> Config:
    config = load()

    profile = inquirer.list_input(
        "Which profile do you want to remove?",
        choices=[p.name for p in config.profiles],
    )

    config.profiles = list(filter(lambda p: p.name != profile, config.profiles))

    config_file.write_bytes(config.json().encode())

    print("[green]🏁 Profile was updated successfully!")
    return config


def _confirm_overwrite() -> None:
    if not inquirer.confirm("Config file already exists, overwrite?"):
        raise typer.Exit(0)


def _get_profile_name(default: str = "Default") -> str:
    return inquirer.text("Profile name", default=default)


def _get_address(default: str = "Kraków") -> str:
    return inquirer.text("Your address", default=default)


def _get_detailed_location(address: str) -> Location:
    return location.get(address)
