"""Test file for Explorer service layer"""

import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.fake.explorer import _explorers, _reset, model_to_dict

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.model.explorer import Explorer
from cryptid.service import explorer

sample = Explorer(
    name="Claude Hande",
    country="FR",
    description="Scarce during full moons",
)


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


def test_get_all():
    got = explorer.get_all()
    assert got == _explorers


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


def test_modify_missing():
    with pytest.raises(MissingError):
        _ = explorer.modify(
            "Iker Jimenez", {"description": "Friend of friends"}
        )


def test_modify_duplicate():
    with pytest.raises(DuplicateError):
        _ = explorer.modify("Claude Hande", {"name": "Noah Weise"})


def test_delete(claude_sample):
    explorer.delete(claude_sample.name)
    with pytest.raises(MissingError):
        explorer.get_one(claude_sample.name)


def test_delete_missing():
    with pytest.raises(MissingError):
        explorer.delete("Iker Jimenez")
