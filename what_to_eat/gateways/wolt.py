import itertools
import urllib.parse
from typing import Final

import httpx
from pydantic import parse_obj_as

from what_to_eat.models.location import Location
from what_to_eat.models.wolt import Item, Restaurant, Section

consumer_wolt_api_url: Final[str] = "https://consumer-api.wolt.com/v1/pages/front"
restaurant_wolt_api_url: Final[str] = "https://restaurant-api.wolt.com/v3/venues/"


class WoltApiError(Exception):
    def __init__(self):
        super().__init__("[Wolt] Error when trying to get response from wolt api")


def sections(location: Location) -> list[Section]:
    params = urllib.parse.urlencode(
        {
            "lat": location.lat,
            "lon": location.lon,
        }
    )

    # TODO: add language to config
    headers = {
        "app-language": "en",
    }
    response = httpx.get(consumer_wolt_api_url, params=params, headers=headers)

    if not response.is_success:
        raise WoltApiError()

    return parse_obj_as(list[Section], response.json()["sections"])


def restaurant(item: Item) -> Restaurant:
    headers = {
        "app-language": "en",
    }
    response = httpx.get(restaurant_wolt_api_url + item.link.target, headers=headers)

    if not response.is_success:
        raise WoltApiError()
    return parse_obj_as(Restaurant, response.json()["results"][0])


def items(location: Location) -> list[Item]:
    return list(
        {
            item
            for item in itertools.chain.from_iterable(
                s.items for s in sections(location)
            )
            if item.venue
        }
    )
