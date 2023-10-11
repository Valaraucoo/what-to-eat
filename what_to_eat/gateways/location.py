import urllib.parse

import httpx

from what_to_eat.models.location import Location
from what_to_eat.utils import cache


class LocationError(Exception):
    def __init__(self):
        super().__init__("Error when trying to get location")


@cache.apply()
def get(address: str) -> Location:
    address = urllib.parse.quote(address)
    response = httpx.get(f"https://nominatim.openstreetmap.org/search?q={address}&format=json")

    if not response.is_success:
        raise LocationError()

    return Location.model_validate(response.json()[0])
