from wte.models import HashableModel


class Location(HashableModel):
    lat: float
    lon: float
