from typing import Final

from wte.models.wolt import Item

default_weight: Final[float] = 20.0


def build_weights(items: list[Item]) -> list[float]:
    return [_build_weight(item) for item in items]


def _build_weight(item: Item) -> float:
    if item.venue and item.venue.rating and item.venue.delivers:
        return item.venue.rating.rating / 3 + item.venue.estimate * 2
    return 20.0
