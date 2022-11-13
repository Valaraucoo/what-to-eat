from what_to_eat.models import HashableModel
from what_to_eat.models.location import Location


class Profile(HashableModel):
    name: str
    is_default: bool = False
    address: str
    location: Location


class Config(HashableModel):
    profiles: list[Profile]
