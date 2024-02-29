"""Test file for User service layer"""

# pylint: disable=C0413:wrong-import-position
import copy
import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.fake.user import _reset, _users, model_to_dict
from cryptid.model.user import User
from cryptid.service import user


@pytest.fixture(name="sample")
def fixture_sample():
    yield User(name="sampleuser", password_hash="samplehash")
    _reset()


@pytest.fixture(name="fakes")
def fixture_fakes():
    yield _users
    _reset()


def test_get_all(fakes):
    got = user.get_all()
    assert got == fakes


def test_get_one_exists(fakes):
    got = user.get_one(fakes[0].name)
    assert got == fakes[0]


def test_get_one_missing():
    with pytest.raises(MissingError):
        user.get_one("non-existentuser")


def test_create(sample):
    got = user.create(sample)
    assert got == sample
    assert user.get_one(sample.name) == sample


def test_create_duplicate(fakes):
    with pytest.raises(DuplicateError):
        user.create(fakes[0])


def test_replace(sample, fakes):
    got = user.replace(fakes[0].name, sample)
    assert got == sample
    assert user.get_one(sample.name) == sample
    with pytest.raises(MissingError):
        user.get_one(fakes[0].name)


def test_replace_missing(sample):
    with pytest.raises(MissingError):
        user.replace(sample.name, sample)


def test_replace_duplicate(fakes):
    with pytest.raises(DuplicateError):
        user.replace(fakes[0].name, fakes[1])


def test_modify(fakes):
    mod_user = User(name=fakes[0].name, password_hash="mod_hash")
    got = user.modify(fakes[0].name, model_to_dict(mod_user))
    assert got == mod_user
    assert user.get_one(mod_user.name) == mod_user


def test_modify_missing(sample):
    with pytest.raises(MissingError):
        user.modify(sample.name, sample)


def test_modify_duplicate(fakes):
    with pytest.raises(DuplicateError):
        user.modify(fakes[0].name, model_to_dict(fakes[1]))


def test_delete(fakes):
    user_to_delete = copy.deepcopy(fakes[0])
    user.delete(fakes[0].name)
    with pytest.raises(MissingError):
        user.get_one(user_to_delete.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        user.delete(sample.name)
