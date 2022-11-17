import urllib.parse

import httpx
from pydantic import parse_obj_as

from what_to_eat.models.location import Location


class LocationError(Exception):
    def __init__(self):
        super().__init__("Error when trying to get location")


def _get(address: str) -> Location:
    address = urllib.parse.quote(address)
    response = httpx.get(f"https://nominatim.openstreetmap.org/search/{address}?format=json")

    if not response.is_success:
        raise LocationError()

    return Location.parse_obj(response.json()[0])


def get(address: str) -> Location:
    return parse_obj_as(Location, _get(address))
