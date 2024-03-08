"""Test file for Creature service layer"""

# pylint: disable=C0413:wrong-import-position
import os

import pytest

from cryptid.data.errors import DuplicateError, MissingError

os.environ["CRYPTID_UNIT_TEST"] = "true"
from cryptid.fake.creature import _creatures, _reset, model_to_dict
from cryptid.model.creature import Creature
from cryptid.service import creature


@pytest.fixture(name="yeti_sample")
def fixture_yeti_sample():
    yield Creature(
        name="Yeti",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
        aka="Abominable Snowman",
    )
    _reset()


@pytest.fixture(name="chupacabra_sample")
def fixture_chupacabra_sample():
    yield Creature(
        name="Chupacabra",
        country="MX",
        area="Sinaloa",
        description="Goat-sucker creature",
        aka="Chupacabras",
    )
    _reset()


@pytest.fixture(name="fakes")
def fixture_fakes():
    yield _creatures
    _reset()


def test_get_all(fakes):
    got = creature.get_all()
    assert got == fakes


def test_get_one_exists(yeti_sample):
    resp = creature.get_one("Yeti")
    assert resp == yeti_sample


def test_get_one_missing():
    with pytest.raises(MissingError):
        creature.get_one("boxturtle")


def test_create(chupacabra_sample):
    resp = creature.create(chupacabra_sample)
    assert resp == chupacabra_sample
    assert creature.get_one(chupacabra_sample.name) == chupacabra_sample


def test_create_duplicate(yeti_sample):
    with pytest.raises(DuplicateError):
        creature.create(yeti_sample)


def test_replace(yeti_sample, chupacabra_sample):
    got = creature.replace(yeti_sample.name, chupacabra_sample)
    assert got == chupacabra_sample
    assert creature.get_one(chupacabra_sample.name) == chupacabra_sample
    with pytest.raises(MissingError):
        creature.get_one("Yeti")


def test_replace_missing(chupacabra_sample):
    with pytest.raises(MissingError):
        creature.replace(chupacabra_sample.name, chupacabra_sample)


def test_replace_duplicate(yeti_sample):
    with pytest.raises(DuplicateError):
        creature.replace("Bigfoot", yeti_sample)


def test_modify(yeti_sample):
    creature.modify(
        yeti_sample.name, {"description": "Abominable hombre de las nieves"}
    )
    mod_yeti = creature.get_one(yeti_sample.name)
    assert mod_yeti.description == "Abominable hombre de las nieves"


def test_modify_missing(chupacabra_sample):
    with pytest.raises(MissingError):
        creature.modify(
            chupacabra_sample.name, model_to_dict(chupacabra_sample)
        )


def test_modify_duplicate(yeti_sample):
    with pytest.raises(DuplicateError):
        creature.modify("Bigfoot", model_to_dict(yeti_sample))


def test_delete(yeti_sample):
    creature.delete(yeti_sample.name)
    with pytest.raises(MissingError):
        creature.get_one(yeti_sample.name)


def test_delete_missing(chupacabra_sample):
    with pytest.raises(MissingError):
        creature.delete(chupacabra_sample.name)
