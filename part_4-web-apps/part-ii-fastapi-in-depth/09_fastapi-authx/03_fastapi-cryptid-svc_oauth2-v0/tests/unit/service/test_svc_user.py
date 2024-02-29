"""Test file for User service layer"""

import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.model.user import User
from cryptid.service import user as service


@pytest.fixture
def sample() -> User:
    return User(name="sampleuser", password_hash="samplehash")


@pytest.fixture
def fakes() -> list[User]:
    return service.get_all()


def test_create(sample):
    got = service.create(sample)
    assert got == sample


def test_create_duplicate(fakes):
    with pytest.raises(DuplicateError):
        service.create(fakes[0])


def test_get_one(fakes):
    got = service.get_one(fakes[0].name)
    assert got == fakes[0]


def test_get_one_missing():
    with pytest.raises(MissingError):
        service.get_one("non-existentuser")


def test_modify(fakes):
    mod_user = User(name=fakes[0].name, password_hash="mod_hash")
    got = service.modify(fakes[0].name, mod_user)
    assert got == mod_user


def test_modify_missing(sample):
    with pytest.raises(MissingError):
        service.modify("non-existent", sample)


def test_modify_duplicate(fakes):
    with pytest.raises(DuplicateError):
        service.modify(fakes[0].name, fakes[1])


def test_delete(fakes):
    service.delete(fakes[0].name)


def test_missing():
    with pytest.raises(MissingError):
        service.delete("non-existent")
