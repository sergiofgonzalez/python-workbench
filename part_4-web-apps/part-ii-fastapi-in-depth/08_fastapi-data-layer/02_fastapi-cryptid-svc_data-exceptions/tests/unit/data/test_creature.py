"""
PyTest unit tests for Creature Data Layer

Note: these tests are executed sequentially from top to bottom, and the db state
is maintained for whole test session.
"""

import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.creature import Creature

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample):
    got = creature.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    with pytest.raises(DuplicateError):
        creature.create(sample)


def test_get_one(sample):
    got = creature.get_one(sample.name)
    assert got == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        creature.get_one("Werewolf")


def test_modify(sample):
    sample.area = "Sesame St."
    got = creature.modify(sample.name, sample)
    assert got == sample


def test_modify_missing():
    critter: Creature = Creature(
        name="Werewolf",
        country="UK",
        area="Highlands",
        description="a wolfman",
        aka="Lupo Hominidus",
    )
    with pytest.raises(MissingError):
        creature.modify(critter.name, critter)


def test_delete(sample):
    creature.delete(sample)
    with pytest.raises(MissingError):
        creature.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        creature.delete(sample)
