"""Fake Explorer data access methods"""

from cryptid.data.errors import DuplicateError, MissingError
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


def get_all() -> list[Explorer]:
    """Return all explorers"""
    return _explorers


def get_one(name: str) -> Explorer:
    """Return the explorer whose name matches the one given"""
    if explorer := _find(name):
        return explorer
    raise MissingError(f"Explorer {name!r} not found")


def create(explorer: Explorer) -> Explorer:
    """
    Adds a new explorer
    """
    _check_duplicate(explorer.name)
    _explorers.append(explorer)
    return explorer


def modify(name: str, explorer_or_dict: Explorer | dict) -> Explorer:
    """
    Partially modifies an explorer.
    """
    saved_explorer = _find(name)
    if not saved_explorer:
        raise MissingError(f"Explorer {name!r} not found")

    if isinstance(explorer_or_dict, dict):
        explorer_dict = explorer_or_dict
        if "name" in explorer_or_dict and name != explorer_dict["name"]:
            _check_duplicate(explorer_dict["name"])
        patched_explorer_dict = model_to_dict(saved_explorer)
        for field in explorer_dict.keys():
            patched_explorer_dict[field] = explorer_dict[field]

        patched_explorer = Explorer(
            name=patched_explorer_dict["name"],
            country=patched_explorer_dict["country"],
            description=patched_explorer_dict["description"],
        )
        _explorers.remove(saved_explorer)
        _explorers.append(patched_explorer)
        return patched_explorer
    elif isinstance(explorer_or_dict, Explorer):
        patched_explorer = explorer_or_dict
        if name != patched_explorer.name:
            _check_duplicate(patched_explorer.name)
        _explorers.remove(saved_explorer)
        _explorers.append(patched_explorer)
        return patched_explorer
    else:
        raise TypeError(f"Invalid type {type(explorer_or_dict)}")


def delete(explorer: Explorer):
    """
    Deletes the explorer given.
    """
    if _find(explorer.name):
        _explorers.remove(explorer)
    else:
        raise MissingError(f"Explorer {explorer.name!r} not found")
