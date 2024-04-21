"""
PyTest unit tests for Creature Data Layer
"""

import os
from typing import Generator

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.creature import Creature

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_UNIT_TEST"] = "true"
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import creature  # pylint: disable=C0413:wrong-import-position


@pytest.fixture(name="sample")
def fixture_sample() -> Generator[Creature, None, None]:
    yield Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )
    creature._reset_table()  # pylint: disable=W0212:protected-access


def test_create(sample):
    got = creature.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    creature.create(sample)
    with pytest.raises(DuplicateError):
        creature.create(sample)


def test_get_one(sample):
    creature.create(sample)
    got = creature.get_one(sample.name)
    assert got == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        creature.get_one("Werewolf")


def test_modify(sample):
    creature.create(sample)
    sample.area = "Sesame St."
    got = creature.modify(sample.name, sample)
    assert got == sample


def test_modify_missing():
    critter: Creature = Creature(
        name="Werewolf",
        country="UK",
        area="Highlands",
        description="a wolfman",
        aka="Lupus Hominidus",
    )
    with pytest.raises(MissingError):
        creature.modify(critter.name, critter)


def test_modify_duplicate(sample):
    creature.create(sample)
    creature.create(
        Creature(
            name="Werewolf",
            country="UK",
            area="Highlands",
            description="a wolfman",
            aka="Lupus Hominidus",
        )
    )
    with pytest.raises(DuplicateError):
        creature.modify("Werewolf", sample)


def test_delete(sample):
    creature.create(sample)
    creature.delete(sample)
    with pytest.raises(MissingError):
        creature.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        creature.delete(sample)
