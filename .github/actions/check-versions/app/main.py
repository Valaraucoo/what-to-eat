import re
from pathlib import Path
from typing import Final

import httpx
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    github_repository: str
    github_ref: str
    github_base_ref: str
    input_github_token: SecretStr


settings: Final[Settings] = Settings()
pyproject_toml: Final[Path] = Path("./pyproject.toml")
what_to_eat_version_file: Final[Path] = Path("./what_to_eat/__init__.py")

version_regex: Final[str] = r"\"(?P<version>[0-9]+\.[0-9]+\.[0-9]+)\""


def get_pyproject_toml_version() -> str:
    content = pyproject_toml.read_text()
    match = re.search(version_regex, content)
    if match is None:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group("version")


def get_what_to_eat_version() -> str:
    content = what_to_eat_version_file.read_text()
    match = re.search(version_regex, content)
    if match is None:
        raise ValueError(f"[{settings.github_ref}] Could not find version in what_to_eat/__init__.py")
    return match.group("version")


def get_master_version() -> str:
    response = httpx.get(f"https://raw.githubusercontent.com/{settings.github_repository}/master/pyproject.toml")
    response.raise_for_status()
    content = response.text
    match = re.search(version_regex, content)
    if match is None:
        raise ValueError("[master] Could not find version in pyproject.toml")
    return match.group("version")


def should_compare_versions() -> bool:
    print(f"Comparing versions for {settings.github_ref} and {settings.github_base_ref}")
    return settings.github_base_ref == "master"


def compare_versions(new: str, old: str) -> bool:
    new = new.split(".")
    old = old.split(".")
    for i in range(3):
        if int(new[i]) > int(old[i]):
            return True
        elif int(new[i]) < int(old[i]):
            return False
    return False


if __name__ == "__main__":
    pyproject_toml_version = get_pyproject_toml_version()
    what_to_eat_version = get_what_to_eat_version()

    if should_compare_versions():
        master_version = get_master_version()
        if compare_versions(pyproject_toml_version, master_version):
            raise ValueError(
                f"Version in pyproject.toml ({pyproject_toml_version}) "
                f"must be greater than version in master ({master_version})"
            )

    if pyproject_toml_version != what_to_eat_version:
        raise ValueError(
            f"Version mismatch between pyproject.toml and what_to_eat/__init__.py: "
            f"{pyproject_toml_version} != {what_to_eat_version}"
        )
