import pytest

from company.common.location import *

@pytest.fixture
def location():
    return Location(
        region=Region.EUROPE,
        country="Belarus",
        city="Minsk",
        street="Dzerzhinskogo",
        building="22A",
    )