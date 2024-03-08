"""Fake Explorer data access methods"""

import os

from cryptid.data.errors import DuplicateError, InvalidStateError, MissingError
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


def _reset():
    """Unit test convenience method that resets the data"""
    global _explorers
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


def _find(name: str) -> Explorer | None:
    for explorer in _explorers:
        if explorer.name == name:
            return explorer


def _check_duplicate(name: str):
    if _find(name):
        raise DuplicateError(f"Explorer {name} already exists")


def model_to_dict(explorer: Explorer) -> dict:
    return explorer.model_dump()


def get_one(name: str) -> Explorer:
    """Return the explorer whose name matches the one given"""
    if explorer := _find(name):
        return explorer
    raise MissingError(f"Explorer {name!r} not found")


def get_all() -> list[Explorer]:
    """Return all explorers"""
    return _explorers


def create(explorer: Explorer) -> Explorer:
    """
    Adds a new explorer
    """
    _check_duplicate(explorer.name)
    _explorers.append(explorer)
    return explorer



def modify(name: str, explorer: Explorer) -> Explorer:
    """
    Replaces the explorer identified by the given name with the information of
    the explorer.
    """
    saved_explorer = _find(name)
    if not saved_explorer:
        raise MissingError(f"Explorer {name!r} not found")
    if name != explorer.name:
        _check_duplicate(explorer.name)
    _explorers.remove(saved_explorer)
    _explorers.append(explorer)
    return explorer


def delete(explorer: Explorer):
    """
    Deletes the given explorer.
    """
    try:
        _explorers.remove(explorer)
    except ValueError as e:
        raise MissingError(f"Explorer {explorer.name!r} not found") from e


if not os.getenv("CRYPTID_UNIT_TEST"):
    raise InvalidStateError("Package intended for unit tests only")
