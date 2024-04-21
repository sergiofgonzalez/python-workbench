"""Fake User data access methods"""

import os

from cryptid.data.errors import DuplicateError, InvalidStateError, MissingError
from cryptid.model.user import User

_users = [
    User(name="user1", password_hash="hash1"),
    User(name="user2", password_hash="hash2"),
]


def _reset():
    """Unit test convenience method that resets the data"""
    global _users
    _users = [
        User(name="user1", password_hash="hash1"),
        User(name="user2", password_hash="hash2"),
    ]


def _find(name: str) -> User | None:
    for e in _users:
        if e.name == name:
            return e
    return None


def _check_missing(name: str):
    if not _find(name):
        raise MissingError(f"Username {name} not found")


def _check_duplicate(name: str):
    if _find(name):
        raise DuplicateError(f"User {name} already exists")


def model_to_dict(user: User) -> dict:
    return user.model_dump()


def get_one(name: str) -> User:
    """Return the user whose name matches the one given"""
    user = _find(name)
    if user:
        return user
    raise MissingError(f"Username {name!r} not found")


def get_all() -> list[User]:
    """Return all users"""
    return _users


def create(user: User, table: str = "user") -> User:
    """
    Adds a new user
    """
    if table not in ("user", "xuser"):
        raise ValueError(f"Unexpected table {table!r}")
    _check_duplicate(user.name)
    _users.append(user)
    return user


def modify(name: str, user: User) -> User:
    """
    Replaces a user identified by the given name, with the given user.
    """
    _check_missing(name)
    # If changing name, will it create a duplicate?
    if name != user.name:
        _check_duplicate(user.name)
    saved_user = _find(name)
    if saved_user:
        _users.remove(saved_user)
        _users.append(user)
        return user
    raise MissingError(f"Username {name} not found")


def delete(user: User):
    """
    Deletes a user
    """
    try:
        _users.remove(user)
    except ValueError as e:
        raise MissingError(f"Username {user.name!r} not found") from e


if not os.getenv("CRYPTID_UNIT_TEST"):
    raise InvalidStateError("Package intended for unit tests only")
