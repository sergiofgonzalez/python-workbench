"""Fake Creature data access methods"""

from cryptid.data.errors import DuplicateError, MissingError
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


def get_all() -> list[Creature]:
    """Return all creatures"""
    return _creatures


def get_one(name: str) -> Creature:
    """Return the creature whose name matches the one given"""
    creature = _find(name)
    if creature:
        return creature
    raise MissingError(f"Creature {name!r} not found")


def create(creature: Creature) -> Creature:
    """
    Adds a new creature
    """
    _check_duplicate(creature.name)
    _creatures.append(creature)
    return creature


def replace(name: str, creature: Creature) -> Creature:
    """
    Replaces a creature with the given one.
    """
    _check_duplicate(creature.name)
    saved_creature = _find(name)
    if not saved_creature:
        raise MissingError(f"Creature {name!r} not found")

    _creatures.remove(saved_creature)
    _creatures.append(creature)
    return creature


def modify(name: str, creature_or_dict: Creature | dict) -> Creature:
    """
    Partially modifies a creature.

    NOTE: the signature of the function reflects that the fakes are used both
    as a data and as a service layer, and the modify function exposes a
    different signature on them.
    """
    saved_creature = _find(name)
    if not saved_creature:
        raise MissingError(f"Creature {name!r} not found")

    if isinstance(creature_or_dict, dict):
        creature_dict = creature_or_dict

        if "name" in creature_dict and name != creature_dict["name"]:
            _check_duplicate(creature_dict["name"])
        patched_creature_dict = model_to_dict(saved_creature)
        for field in creature_dict.keys():
            patched_creature_dict[field] = creature_dict[field]

        patched_creature = Creature(
            name=patched_creature_dict["name"],
            country=patched_creature_dict["country"],
            description=patched_creature_dict["description"],
            aka=patched_creature_dict["aka"],
            area=patched_creature_dict["area"],
        )
        _creatures.remove(saved_creature)
        _creatures.append(patched_creature)
        return patched_creature
    elif isinstance(creature_or_dict, Creature):
        creature: Creature = creature_or_dict
        if creature.name != name:
            _check_duplicate(creature.name)
        _creatures.remove(saved_creature)
        _creatures.append(creature)
        return creature
    else:
        raise TypeError(f"Unexpected type {type(creature_or_dict)}")


def delete(creature_or_name: Creature | str):
    """
    Deletes the creature given.
    """
    if isinstance(creature_or_name, Creature):
        name = creature_or_name.name
    elif isinstance(creature_or_name, str):
        name = creature_or_name
    else:
        raise TypeError(f"Unexpected type {type(creature_or_name)}")

    if creature := _find(name):
        _creatures.remove(creature)
    else:
        raise MissingError(f"Creature {name!r} not found")
