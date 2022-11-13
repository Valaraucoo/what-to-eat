from what_to_eat.models import HashableModel


class Location(HashableModel):
    lat: float
    lon: float
