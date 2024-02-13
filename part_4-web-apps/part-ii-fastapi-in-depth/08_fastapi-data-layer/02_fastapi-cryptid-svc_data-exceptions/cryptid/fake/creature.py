"""Fake Creature data access methods"""

from cryptid.model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Bigfoot",
        aka="Yeti's cousin Eddie",
        country="US",
        area="*",
        description="Sasquatch",
    ),
]


def get_all() -> list[Creature]:
    """Return all creatures"""
    return _creatures


def get_one(name: str) -> Creature | None:
    """Return the creature whose name matches the one given"""
    for creature in _creatures:
        if creature.name == name:
            return creature
    return None


def create(creature: Creature) -> Creature:
    """
    Adds a new creature

    NOTE: for now, the given creature is not added to the list
    """
    return creature


def modify(creature: Creature) -> Creature:
    """
    Partially modifies a creature

    NOTE: for now, the given creature is not modified in the list
    """
    return creature


def replace(creature: Creature) -> Creature:
    """
    Completely replaces an explorer

    NOTE: for now, the given creature is not replaced in the list
    """
    return creature


def delete(name: str) -> bool:
    """
    Deletes a creature given its name and returns None if it existed

    NOTE: for now, the given explorer is not removed from the list
    """
    return None
