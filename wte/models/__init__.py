from enum import Enum

from pydantic import BaseModel


class HashableModel(BaseModel):
    def __hash__(self) -> int:
        return hash(self.json())


class Sort(str, Enum):
    NONE = "none"
    RESTAURANT = "restaurant"
    ADDRESS = "address"
    DELIVERY_COST = "delivery_cost"
    ESTIMATE_TIME = "estimate_time"
    RATING = "rating"
    PRICE = "price"

    @classmethod
    def choices(cls) -> list[str]:
        return list(cls)


class Ordering(str, Enum):
    ASC = "asc"
    DESC = "desc"

    @classmethod
    def choices(cls) -> list[str]:
        return list(cls)
