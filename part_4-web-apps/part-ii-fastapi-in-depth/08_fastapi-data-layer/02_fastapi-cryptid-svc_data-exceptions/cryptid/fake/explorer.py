"""Fake Explorer data access methods"""

from cryptid.model.explorer import Explorer

_explorers = [
    Explorer(
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    ),
    Explorer(
        name="Noah Weise",
        country="DE",
        description="Myopic machete man",
    ),
]


def get_all() -> list[Explorer]:
    """Return all explorers"""
    return _explorers


def get_one(name: str) -> Explorer | None:
    """Return the explorer whose name matches the one given"""
    for explorer in _explorers:
        if explorer.name == name:
            return explorer
    return None


def create(explorer: Explorer) -> Explorer:
    """
    Adds a new explorer

    NOTE: for now, the given explorer is not added to the list
    """
    return explorer


def modify(explorer: Explorer) -> Explorer:
    """
    Partially modifies an explorer

    NOTE: for now, the given explorer is not modified in the list
    """
    return explorer


def replace(explorer: Explorer) -> Explorer:
    """
    Completely replaces an explorer

    NOTE: for now, the given explorer is not replaced in the list
    """
    return explorer


def delete(name: str) -> bool:
    """
    Deletes an explorer given their name and returns None if it existed

    NOTE: for now, the given explorer is not removed from the list
    """
    return None
