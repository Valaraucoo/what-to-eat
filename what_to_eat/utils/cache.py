from __future__ import annotations

import pickle
import time
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Final, TypeAlias, TypeVar

from what_to_eat.models import HashableModel

default_app_dir: Final[Path] = Path.home() / ".what-to-eat"
cache_file: Final[Path] = default_app_dir / ".what-to-eat-cache.json"
two_minutes: Final[int] = 2 * 60

Key: TypeAlias = str
T = TypeVar("T")


class Cache(HashableModel):
    expires: int
    data: dict[Key, Any]

    def is_expired(self) -> bool:
        return self.expires < int(time.time())

    def get(self, key: Key) -> Any | None:
        return self.data.get(key)

    def set(self, key: Key, value: Any) -> None:
        self.data[key] = value

    def save(self) -> None:
        cache_file.write_bytes(self.dumps())

    def dumps(self) -> bytes:
        return pickle.dumps(self)

    @classmethod
    def load(cls) -> Cache:
        if not cache_file.is_file():
            return cls(expires=int(time.time()) + two_minutes, data={})
        return pickle.loads(cache_file.read_bytes())


def default_key(func: Callable[..., T], *args: Any, **kwargs: Any) -> Key:
    return func.__name__ + str(args) + str(kwargs)


def apply(key: Callable[..., Key] = default_key) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def inner(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            cache = Cache.load()
            if cache.is_expired():
                cache = Cache(expires=int(time.time()) + two_minutes, data={})

            _key = key(func, *args, **kwargs)
            if value := cache.get(_key):
                return value

            value = func(*args, **kwargs)
            cache.set(_key, value)
            cache.save()
            return value

        return wrapper

    return inner
