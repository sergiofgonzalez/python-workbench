"""Test file for Creature service layer"""

from cryptid.model.creature import Creature
from cryptid.service import creature

sample = Creature(
    name="Yeti",
    country="CN",
    area="Himalayas",
    description="Hirsute Himalayan",
    aka="Abominable Snowman",
)


def test_create():
    resp = creature.create(sample)
    assert resp == sample


def test_get_exists():
    resp = creature.get_one("Yeti")
    assert resp == sample


def test_get_missing():
    resp = creature.get_one("boxturtle")
    assert resp is None
