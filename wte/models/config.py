from wte.models import HashableModel
from wte.models.location import Location


class Profile(HashableModel):
    name: str
    is_default: bool = False
    address: str
    location: Location


class Config(HashableModel):
    profiles: list[Profile]
