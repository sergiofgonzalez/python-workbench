"""Test file for Creature web layer"""

import os
from copy import copy
from typing import Generator

import pytest
from fastapi import HTTPException

from cryptid.fake.creature import _reset
from cryptid.model.creature import Creature

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.web import creature  # pylint: disable=C0413:wrong-import-position


@pytest.fixture(name="sample")
def fixture_dragon_sample() -> Generator[Creature, None, None]:
    yield Creature(
        name="Dragon",
        description="A large creature with wings that expels fire",
        country="*",
        area="*",
        aka="firedrake",
    )
    _reset()


@pytest.fixture(name="fakes")
def fixture_fakes() -> Generator[list[Creature], None, None]:
    yield creature.get_all()
    _reset()


def test_get_all(fakes: list[Creature]):
    assert len(fakes) > 0
    assert fakes == creature.get_all()


def test_get_one(fakes):
    got = creature.get_one(fakes[0].name)
    assert got == fakes[0]


def test_get_one_missing(sample: Creature):
    with pytest.raises(HTTPException) as e:
        creature.get_one(sample.name)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_create(sample: Creature):
    got = creature.create(sample)
    assert got == sample
    assert got in creature.get_all()


def test_create_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        creature.create(fakes[0])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
    assert fakes[0].name in e.value.detail


def test_modify(fakes):
    got = creature.modify(
        fakes[0].name,
        {
            "name": "modname",
            "country": "XY",
            "area": "ZZ",
            "description": "moddesc",
            "aka": "modaka",
        },
    )
    assert got.name == "modname"
    assert got.country == "XY"
    assert got.area == "ZZ"
    assert got.description == "moddesc"
    assert got.aka == "modaka"


def test_modify_missing(sample: Creature):
    with pytest.raises(HTTPException) as e:
        creature.modify(sample.name, {})

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_modify_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        creature.modify(fakes[0].name, {"name": fakes[1].name})

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
    assert fakes[1].name in e.value.detail


def test_replace(fakes, sample):
    to_be_replaced_fake = copy(fakes[0])
    got = creature.replace(fakes[0].name, sample)
    assert got == sample
    assert got in creature.get_all()
    assert to_be_replaced_fake not in creature.get_all()


def test_replace_missing(sample: Creature):
    with pytest.raises(HTTPException) as e:
        creature.replace(sample.name, sample)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
    assert sample.name in e.value.detail


def test_replace_duplicate(fakes):
    with pytest.raises(HTTPException) as e:
        creature.replace(fakes[0].name, fakes[1])

    assert e.value.status_code == 409
    assert "already exists" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
    assert fakes[1].name in e.value.detail


def test_delete(fakes):
    to_be_deleted_fake = copy(fakes[0])
    creature.delete(fakes[0].name)
    assert to_be_deleted_fake not in creature.get_all()


def test_delete_missing(sample):
    with pytest.raises(HTTPException) as e:
        creature.delete(sample.name)

    assert e.value.status_code == 404
    assert "not found" in e.value.detail.lower()
    assert "creature" in e.value.detail.lower()
