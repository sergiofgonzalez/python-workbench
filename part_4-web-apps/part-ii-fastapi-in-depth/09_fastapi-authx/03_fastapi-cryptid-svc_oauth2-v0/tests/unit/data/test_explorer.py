"""
PyTest unit tests for Explorer Data Layer

Note: these tests are executed sequentially from top to bottom, and the db state
is maintained for whole test session.
"""

import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.explorer import Explorer

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import explorer


@pytest.fixture
def sample() -> Explorer:
    return Explorer(
        name="Van Helsing",
        country="NL",
        description="Vampire slayer"
    )


def test_create(sample):
    got = explorer.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    with pytest.raises(DuplicateError):
        explorer.create(sample)


def test_get_one(sample):
    got = explorer.get_one(sample.name)
    assert got == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        explorer.get_one("Werewolf")


def test_modify(sample):
    sample.country = "UK"
    got = explorer.modify(sample.name, sample)
    assert got == sample


def test_modify_missing():
    gizmo: Explorer = Explorer(
        name="Guillermo de la Cruz",
        country="MX",
        description="Nandor's familiar",
    )
    with pytest.raises(MissingError):
        explorer.modify(gizmo.name, gizmo)


def test_delete(sample):
    explorer.delete(sample)
    with pytest.raises(MissingError):
        explorer.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        explorer.delete(sample)
