import re
from pathlib import Path
from typing import Final

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    github_repository: str
    github_ref: str
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
        raise ValueError("Could not find version in what_to_eat/__init__.py")
    return match.group("version")


if __name__ == "__main__":
    pyproject_toml_version = get_pyproject_toml_version()
    what_to_eat_version = get_what_to_eat_version()
    if pyproject_toml_version != what_to_eat_version:
        raise ValueError(
            f"Version mismatch between pyproject.toml and what_to_eat/__init__.py: "
            f"{pyproject_toml_version} != {what_to_eat_version}"
        )
