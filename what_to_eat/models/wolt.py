import datetime
from enum import Enum
from typing import TypeAlias

from pydantic import HttpUrl

from what_to_eat.models import HashableModel


class Rating(HashableModel):
    rating: float
    score: float


class RatingDetail(HashableModel):
    negative_percentage: int
    neutral_percentage: int
    positive_percentage: int
    rating: int
    score: int
    text: str
    volume: int


class Venue(HashableModel):
    name: str
    address: str
    country: str
    currency: str
    delivery_price_int: int
    estimate_range: str
    estimate: float
    delivers: bool
    short_description: str | None
    tags: list[str]
    rating: Rating | None
    price_range: int

    def format_tags(self) -> str:
        return ", ".join(map(str.capitalize, self.tags))

    def format_address(self) -> str:
        return self.address

    def format_estimate_range(self) -> str:
        if not self.estimate_range:
            return "-"
        return self.estimate_range.replace("-", " - ") + " min"

    def format_delivery_price(self) -> str:
        if self.delivery_price_int is None:
            return "-"
        if not self.delivers:
            return "(No delivery)"
        return f"{self.delivery_price_int / 100:.2f} {self.currency}"

    def format_rating(self) -> str:
        if not self.rating:
            return "-"
        return str(self.rating.score)

    def format_price_range(self) -> str:
        if not self.price_range:
            return "-"
        return ":money_bag:" * self.price_range


class Link(HashableModel):
    target: str


class Item(HashableModel):
    title: str
    track_id: str
    link: Link
    venue: Venue | None = None


class Section(HashableModel):
    name: str
    title: str | None
    items: list[Item] = []


class Translation(HashableModel):
    lang: str
    value: str


Weekday: TypeAlias = str


class TimesType(str, Enum):
    OPEN = "open"
    CLOSE = "close"


class Times(HashableModel):
    type: str
    value: dict[str, int]

    def format(self) -> str:
        if not (value := self.value.get("$date")):
            return "-"
        return datetime.datetime.fromtimestamp(value / 1000).strftime("%H:%M")


class Statistics(HashableModel):
    mean: int | None
    max: int | None
    min: int | None


class Estimates(HashableModel):
    delivery: Statistics
    pickup: Statistics
    preparation: Statistics
    total: Statistics

    def format(self) -> str:
        if not self.total.mean:
            return "-"
        return f"{self.total.mean} minutes"


class Restaurant(HashableModel):
    name: list[Translation]
    address: str
    city: str
    country: str
    currency: str
    food_tags: list[str]
    phone: str | None
    price_range: int
    public_url: HttpUrl
    rating: RatingDetail | None
    website: HttpUrl | None
    allowed_payment_methods: list[str]
    description: list[Translation]
    estimates: Estimates | None
    opening_times: dict[Weekday, list[Times]] = {}

    def format_estimates(self) -> str:
        if not self.estimates:
            return "-"
        return self.estimates.format()

    def format_description(self) -> str:
        if not self.description:
            return "-"
        description = self.description[0].value
        if len(description) > 30:
            description = description[:60] + "..."
        return description

    def format_opening_time(self) -> str:
        weekday = datetime.datetime.now().strftime("%A").lower()
        opening_times = self.opening_times.get(weekday)
        if not opening_times:
            return "-"

        open_time = next(time for time in opening_times if time.type == TimesType.OPEN)
        close_time = next(time for time in opening_times if time.type == TimesType.CLOSE)

        return f"{open_time.format()} - {close_time.format()}"

    def format_name(self) -> str:
        return f":pizza: [u]{self.name[0].value}[/u]"

    def format_address(self) -> str:
        return f"[u]{self.city}, {self.address}[/u] :pizza:"

    def format_price_range(self) -> str:
        if not self.price_range:
            return "-"
        return ":money_bag:" * self.price_range

    def format_phone(self) -> str:
        return f"{self.phone[:3]} {self.phone[3:]}"

    def format_public_url(self) -> str:
        return self.public_url

    def format_rating(self) -> str:
        if not self.rating:
            return "-"
        return f"{self.rating.text} ({self.rating.score} / {self.rating.volume} reviews)"

    def format_tags(self) -> str:
        return ", ".join(f"[black on yellow]{tag.capitalize()}[/]" for tag in self.food_tags)

    def format_allowed_payment_methods(self) -> str:
        return ", ".join(map(str.capitalize, self.allowed_payment_methods))
