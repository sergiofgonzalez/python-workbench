"""
PyTest unit tests for Explorer Data Layer
"""

import os
from typing import Generator

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.explorer import Explorer

# Setting SQLite in-memory mode before importing the Data Layer
os.environ["CRYPTID_UNIT_TEST"] = "true"
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"
from cryptid.data import explorer  # pylint: disable=C0413:wrong-import-position


@pytest.fixture(name="sample")
def fixture_sample() -> Generator[Explorer, None, None]:
    yield Explorer(
        name="Van Helsing", country="NL", description="Vampire slayer"
    )
    explorer._reset_table()  # pylint: disable=W0212:protected-access


def test_create(sample):
    got = explorer.create(sample)
    assert got == sample


def test_create_duplicate(sample):
    explorer.create(sample)

    with pytest.raises(DuplicateError):
        explorer.create(sample)


def test_get_one(sample):
    explorer.create(sample)

    got = explorer.get_one(sample.name)
    assert got == sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        explorer.get_one("Guillermo de la Cruz")


def test_modify(sample):
    explorer.create(sample)
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


def test_modify_duplicate(sample):
    explorer.create(sample)
    explorer.create(
        Explorer(
            name="Guillermo de la Cruz",
            country="MX",
            description="Nandor's familiar",
        )
    )
    with pytest.raises(DuplicateError):
        explorer.modify("Guillermo de la Cruz", sample)


def test_delete(sample):
    explorer.create(sample)
    explorer.delete(sample)
    with pytest.raises(MissingError):
        explorer.get_one(sample.name)


def test_delete_missing(sample):
    with pytest.raises(MissingError):
        explorer.delete(sample)
