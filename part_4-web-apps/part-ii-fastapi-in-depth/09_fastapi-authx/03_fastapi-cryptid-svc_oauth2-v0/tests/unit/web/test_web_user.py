"""Test file for User web layer"""

import os
from copy import copy
from typing import Generator

import pytest
from fastapi import HTTPException

from cryptid.fake.user import _reset
from cryptid.model.user import User

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.web import user  # pylint: disable=C0413:wrong-import-position


@pytest.fixture(name="sample")
def fixture_sample() -> Generator[User, None, None]:
    yield User(name="sample_user", password_hash="sample_hash")
    _reset()


@pytest.fixture(name="fakes")
def fixture_fakes() -> Generator[list[User], None, None]:
    yield user.get_all()
    _reset()


def test_get_all(fakes: list[User]):
    assert len(fakes) > 0
    assert fakes == user.get_all()


def test_get_one(fakes):
    got = user.get_one(fakes[0].name)
    assert got == fakes[0]


def test_get_one_missing(sample: User):
    with pytest.raises(HTTPException) as e:
        user.get_one(sample.name)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_create(sample: User):
    got = user.create(sample)
    assert got == sample
    assert got in user.get_all()


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        user.create(fakes[0])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
    assert fakes[0].name in e.value.detail


def test_modify(fakes):
    got = user.modify(
        fakes[0].name,
        User(name="mod_username", password_hash="mod_password_hash")
    )
    assert got.name == "mod_username"
    assert got.password_hash == "mod_password_hash"


def test_modify_missing(sample: User):
    with pytest.raises(HTTPException) as e:
        user.modify(sample.name, sample)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_modify_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        user.modify(fakes[0].name, fakes[1])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
    assert fakes[1].name in e.value.detail


def test_replace(fakes, sample):
    to_be_replaced_fake = copy(fakes[0])
    got = user.replace(fakes[0].name, sample)
    assert got == sample
    assert got in user.get_all()
    assert to_be_replaced_fake not in user.get_all()


def test_replace_missing(sample: User):
    with pytest.raises(HTTPException) as e:
        user.replace(sample.name, sample)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_replace_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        user.replace(fakes[0].name, fakes[1])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
    assert fakes[1].name in e.value.detail


def test_delete(fakes):
    to_be_deleted_fake = copy(fakes[0])
    user.delete(fakes[0].name)
    assert to_be_deleted_fake not in user.get_all()


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as e:
        user.delete(sample.name)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "user" in e.value.detail.lower()
