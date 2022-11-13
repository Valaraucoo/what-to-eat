from unittest import mock

import pytest

from tests.factories import ItemFactory, ProfileFactory


@pytest.fixture
def mock_find_profile() -> None:
    with mock.patch("what_to_eat.services.profile.find_profile") as mocked_find_profile:
        mocked_find_profile.return_value = ProfileFactory.create()
        yield mocked_find_profile


@pytest.fixture
def mock_wolt_items() -> None:
    with mock.patch("what_to_eat.gateways.wolt.items") as mocked_wolt_items:
        mocked_wolt_items.return_value = [
            ItemFactory.create() for _ in range(10)
        ]
        yield mocked_wolt_items
