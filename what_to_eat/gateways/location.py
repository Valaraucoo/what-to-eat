import httpx
import urllib.parse

from what_to_eat.models.location import Location


class LocationError(Exception):
    def __init__(self):
        super().__init__("Error when trying to get location")


def get(address: str) -> Location:
    address = urllib.parse.quote(address)
    response = httpx.get(f"https://nominatim.openstreetmap.org/search/{address}?format=json")

    if not response.is_success:
        raise LocationError()

    return Location.parse_obj(response.json()[0])
