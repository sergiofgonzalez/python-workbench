"""pytest unit tests for creature.py."""

import pytest

from utils.creature import Creature


@pytest.fixture(name="dragon")
def fixture_dragon_sample() -> Creature:
    """Fixture providing a sample Creature instance representing a dragon."""
    return Creature(
        name="Dragon",
        description=(
            "A large, serpentine legendary creature that appears in the"
            " folklore of many cultures around the world."
        ),
        country="*",
        area="Mountains, Caves",
        aka="Drake, Wyrm",
    )


def test_dragon_attributes(dragon: Creature) -> None:
    """Test to verify the attributes of the dragon Creature instance."""
    assert dragon.name == "Dragon"
    assert dragon.description.startswith("A large, serpentine legendary creature")
    assert dragon.country == "*"
    assert dragon.area == "Mountains, Caves"
    assert dragon.aka == "Drake, Wyrm"
