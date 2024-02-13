"""Creature service layer"""

import cryptid.fake.creature as data
from cryptid.model.creature import Creature


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(creature_id) -> Creature | None:
    return data.get_one(creature_id)


def create(creature: Creature) -> Creature:
    return data.create(creature)


def replace(creature_id, creature: Creature) -> Creature:
    return data.replace(creature_id, creature)


def modify(creature_id, creature: Creature) -> Creature:
    return data.modify(creature_id, creature)


def delete(creature_id) -> bool:
    return data.delete(creature_id)
