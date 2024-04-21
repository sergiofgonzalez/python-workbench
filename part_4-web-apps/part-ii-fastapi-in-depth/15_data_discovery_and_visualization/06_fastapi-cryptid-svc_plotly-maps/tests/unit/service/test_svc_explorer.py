"""Test file for Explorer service layer"""

# pylint: disable=C0413:wrong-import-position
import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.fake.explorer import _explorers, _reset, model_to_dict
from cryptid.model.explorer import Explorer
from cryptid.service import explorer


@pytest.fixture(name="claude_sample")
def fixture_claude_sample():
    yield Explorer(
        name="Claude Hande",
        country="FR",
        description="Scarce during full moons",
    )
    _reset()


@pytest.fixture(name="helsing_sample")
def fixture_helsing_sample():
    yield Explorer(
        name="Van Helsing",
        country="NL",
        description="Vampire slayer",
    )
    _reset()


@pytest.fixture(name="fakes")
def fixture_fakes():
    yield _explorers
    _reset()


def test_get_all(fakes):
    got = explorer.get_all()
    assert got == fakes


def test_get_one_exists(claude_sample):
    got = explorer.get_one(claude_sample.name)
    assert got == claude_sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        explorer.get_one("Iker Jimenez")


def test_create(helsing_sample):
    got = explorer.create(helsing_sample)
    assert got == helsing_sample


def test_create_duplicate(claude_sample):
    with pytest.raises(DuplicateError):
        explorer.create(claude_sample)
    _reset()


def test_replace_happy_path(claude_sample, helsing_sample):
    got = explorer.replace(claude_sample.name, helsing_sample)
    assert got == helsing_sample
    assert explorer.get_one(helsing_sample.name) == helsing_sample
    with pytest.raises(MissingError):
        explorer.get_one(claude_sample.name)


def test_replace_missing(claude_sample):
    with pytest.raises(MissingError):
        explorer.replace("Iker Jimenez", claude_sample)


def test_replace_duplicate(claude_sample):
    with pytest.raises(DuplicateError):
        explorer.replace("Noah Weise", claude_sample)


def test_modify_happy_path(claude_sample):
    _ = explorer.modify(
        claude_sample.name, {"description": "Friend of friends"}
    )
    mod_claude = explorer.get_one(claude_sample.name)
    assert mod_claude.description == "Friend of friends"


def test_modify_missing(helsing_sample):
    with pytest.raises(MissingError):
        _ = explorer.modify("Iker Jimenez", model_to_dict(helsing_sample))


def test_modify_duplicate(claude_sample):
    with pytest.raises(DuplicateError):
        _ = explorer.modify("Noah Weise", model_to_dict(claude_sample))


def test_delete(claude_sample):
    explorer.delete(claude_sample.name)
    with pytest.raises(MissingError):
        explorer.get_one(claude_sample.name)


def test_delete_missing():
    with pytest.raises(MissingError):
        explorer.delete("Iker Jimenez")
