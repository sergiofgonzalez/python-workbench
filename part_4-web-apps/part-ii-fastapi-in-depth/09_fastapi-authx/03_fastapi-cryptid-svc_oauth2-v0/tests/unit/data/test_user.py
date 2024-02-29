"""
PyTest unit tests for the User Data Layer

Note: these tests are executed sequentially from top to bottom, and the db state
is maintained for whole test session.
"""

import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.user import User

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import user


@pytest.fixture
def sample() -> User:
    return User(
        name="user1",
        password_hash="hash1",
    )


def test_create(sample):
    got = user.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    with pytest.raises(DuplicateError):
        user.create(sample)


def test_get_one(sample):
    got = user.get_one(sample.name)
    assert got == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        user.get_one("user2")


def test_modify(sample):
    sample.password_hash = "new_hash"
    got = user.modify(sample.name, sample)
    assert got == sample


def test_modify_missing():
    new_user: User = User(
        name="user2",
        password_hash="hash2",
    )
    with pytest.raises(MissingError):
        user.modify(new_user.name, new_user)


def test_delete(sample):
    user.delete(sample)
    with pytest.raises(MissingError):
        user.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        user.delete(sample)
