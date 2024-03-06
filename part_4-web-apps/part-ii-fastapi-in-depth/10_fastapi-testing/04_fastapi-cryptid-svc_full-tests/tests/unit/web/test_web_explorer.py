"""Test file for Explorer web layer"""

# pylint: disable=C0413:wrong-import-position
import os
from copy import copy
from typing import Generator

import pytest
from fastapi import HTTPException

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.fake.explorer import _reset
from cryptid.model.explorer import Explorer
from cryptid.web import explorer  # pylint: disable=C0413:wrong-import-position


@pytest.fixture(name="sample")
def fixture_iker_sample() -> Generator[Explorer, None, None]:
    yield Explorer(
        name="Iker Jimenez",
        description="Journalist seeking cryptids",
        country="ES",
    )
    _reset()


@pytest.fixture(name="fakes")
def fixture_fakes() -> Generator[list[Explorer], None, None]:
    yield explorer.get_all()
    _reset()


def test_get_all(fakes: list[Explorer]):
    assert len(fakes) > 0
    assert fakes == explorer.get_all()


def test_get_one(fakes):
    got = explorer.get_one(fakes[0].name)
    assert got == fakes[0]


def test_get_one_missing(sample: Explorer):
    with pytest.raises(HTTPException) as e:
        explorer.get_one(sample.name)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_create(sample: Explorer):
    got = explorer.create(sample)
    assert got == sample
    assert got in explorer.get_all()


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        explorer.create(fakes[0])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
    assert fakes[0].name in e.value.detail


def test_modify(fakes):
    got = explorer.modify(
        fakes[0].name,
        {
            "name": "modname",
            "country": "XY",
            "description": "moddesc",
        },
    )
    assert got.name == "modname"
    assert got.country == "XY"
    assert got.description == "moddesc"


def test_modify_missing(sample: Explorer):
    with pytest.raises(HTTPException) as e:
        explorer.modify(sample.name, {})

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_modify_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        explorer.modify(fakes[0].name, {"name": fakes[1].name})

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
    assert fakes[1].name in e.value.detail


def test_replace(fakes, sample):
    to_be_replaced_fake = copy(fakes[0])
    got = explorer.replace(fakes[0].name, sample)
    assert got == sample
    assert got in explorer.get_all()
    assert to_be_replaced_fake not in explorer.get_all()


def test_replace_missing(sample: Explorer):
    with pytest.raises(HTTPException) as e:
        explorer.replace(sample.name, sample)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_replace_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        explorer.replace(fakes[0].name, fakes[1])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
    assert fakes[1].name in e.value.detail


def test_delete(fakes):
    to_be_deleted_fake = copy(fakes[0])
    explorer.delete(fakes[0].name)
    assert to_be_deleted_fake not in explorer.get_all()


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as e:
        explorer.delete(sample.name)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "explorer" in e.value.detail.lower()
