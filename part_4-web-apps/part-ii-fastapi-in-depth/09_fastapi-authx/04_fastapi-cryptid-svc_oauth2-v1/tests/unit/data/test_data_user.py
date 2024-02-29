"""
PyTest unit tests for the User Data Layer

Note: these tests are executed sequentially from top to bottom, and the db state
is maintained for whole test session.
"""

import os
from typing import Generator

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.user import User

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_UNIT_TEST"] = "true"
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import user  # pylint: disable=C0413:wrong-import-position


@pytest.fixture(name="sample")
def fixture_sample() -> Generator[User, None, None]:
    yield User(
        name="user1",
        password_hash="hash1",
    )
    user._reset_table()  # pylint: disable=W0212:protected-access


def test_create(sample):
    got = user.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    user.create(sample)
    with pytest.raises(DuplicateError):
        user.create(sample)


def test_get_one(sample):
    user.create(sample)
    got = user.get_one(sample.name)
    assert got == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        user.get_one("user2")


def test_modify(sample):
    user.create(sample)
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


def test_modify_duplicate(sample):
    user.create(sample)
    user.create(
        User(
            name="user2",
            password_hash="hash2",
        )
    )
    with pytest.raises(DuplicateError):
        user.modify("user2", sample)


def test_delete(sample):
    user.create(sample)
    user.delete(sample)
    with pytest.raises(MissingError):
        user.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        user.delete(sample)
