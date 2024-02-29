"""Fake User data access methods"""

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.user import User

_fakes = [
    User(name="user1", password_hash="hash1"),
    User(name="user2", password_hash="hash2"),
]


def _reset():
    """Unit test convenience method that resets the data"""
    global _fakes
    _fakes = [
        User(name="user1", password_hash="hash1"),
        User(name="user2", password_hash="hash2"),
    ]


def _find(name: str) -> User | None:
    for e in _fakes:
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


def get_all() -> list[User]:
    """Return all users"""
    return _fakes


def get_one(name: str) -> User:
    """Return the user whose name matches the one given"""
    user = _find(name)
    if user:
        return user
    raise MissingError(f"Username {name} not found")


def create(user: User) -> User:
    """
    Adds a new user
    """
    _check_duplicate(user.name)
    _fakes.append(user)
    return user


def modify(name: str, user: User) -> User:
    """
    Partially modifies an user
    """
    _check_missing(name)
    # If changing name, will it create a duplicate?
    if name != user.name:
        _check_duplicate(user.name)
    saved_user = _find(name)
    if saved_user:
        _fakes.remove(saved_user)
        _fakes.append(user)
        return user
    raise MissingError(f"Username {name} not found")


def delete(name_or_user: str | User):
    """
    Deletes a user
    """
    if isinstance(name_or_user, User):
        user = name_or_user
        _check_missing(user.name)
        found_user = _find(user.name)
        if found_user:
            _fakes.remove(found_user)
    elif isinstance(name_or_user, str):
        name = name_or_user
        _check_missing(name)
        found_user = _find(name)
        if found_user:
            _fakes.remove(found_user)
    else:
        raise TypeError("name_or_user must be a User or a string")


# Functions that are used in other layers but not implemented in the fake
# implementation.
def auth_user(name: str, plain: str) -> User | None:
    raise NotImplementedError


def create_access_token(info, expires):
    raise NotImplementedError
