from factory import Factory

from wte.models.config import Config, Profile
from wte.models.location import Location
from wte.models.wolt import Item, Venue


class ConfigFactory(Factory):
    class Meta:
        model = Config

    profiles = [Profile(name="default", address="Test address", location=Location(lat=0.0, lon=0.0), is_default=True)]


class ProfileFactory(Factory):
    class Meta:
        model = Profile

    name = "default"
    address = "Test address"
    location = Location(lat=0.0, lon=0.0)
    is_default = True


class ItemFactory(Factory):
    class Meta:
        model = Item


class VenueFactory(Factory):
    class Meta:
        model = Venue
