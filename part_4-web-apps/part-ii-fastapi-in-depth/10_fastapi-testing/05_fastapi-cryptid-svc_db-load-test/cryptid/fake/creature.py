"""Fake Creature data access methods"""

import os

from cryptid.data.errors import DuplicateError, InvalidStateError, MissingError
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


def _reset():
    """Unit test convenience method that resets the data"""
    global _creatures
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


def _find(name: str) -> Creature | None:
    for creature in _creatures:
        if creature.name == name:
            return creature
    return None


def _check_duplicate(name: str):
    if _find(name):
        raise DuplicateError(f"Creature {name!r} already exists")


def model_to_dict(creature: Creature) -> dict:
    return creature.model_dump()


def get_one(name: str) -> Creature:
    """Return the creature whose name matches the one given"""
    creature = _find(name)
    if creature:
        return creature
    raise MissingError(f"Creature {name!r} not found")


def get_all() -> list[Creature]:
    """Return all creatures"""
    return _creatures


def create(creature: Creature) -> Creature:
    """
    Adds a new creature
    """
    _check_duplicate(creature.name)
    _creatures.append(creature)
    return creature


def modify(name: str, creature: Creature) -> Creature:
    """
    Replaces the creature identified by the given name with the
    information of the creature.
    """
    saved_creature = _find(name)
    if not saved_creature:
        raise MissingError(f"Creature {name!r} not found")

    if creature.name != name:
        _check_duplicate(creature.name)
    _creatures.remove(saved_creature)
    _creatures.append(creature)
    return creature


def delete(creature: Creature):
    try:
        _creatures.remove(creature)
    except ValueError as e:
        raise MissingError(f"Creature {creature.name!r} not found") from e


if not os.getenv("CRYPTID_UNIT_TEST"):
    raise InvalidStateError("Package intended for unit tests only")
