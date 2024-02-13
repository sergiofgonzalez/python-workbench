"""Creature service layer"""

import cryptid.data.creature as data
from cryptid.model.creature import Creature


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(creature_id) -> Creature:
    return data.get_one(creature_id)


def create(creature: Creature) -> Creature:
    return data.create(creature)


def replace(creature_id, creature: Creature) -> Creature:
    return data.modify(creature_id, creature)


def modify(creature_id, creature_dict: dict) -> Creature:
    patched_creature_dict = data.model_to_dict(data.get_one(creature_id))
    for field in creature_dict.keys():
        patched_creature_dict[field] = creature_dict[field]

    return data.modify(
        creature_id,
        Creature(
            name=patched_creature_dict["name"],
            country=patched_creature_dict["country"],
            description=patched_creature_dict["description"],
            aka=patched_creature_dict["aka"],
            area=patched_creature_dict["area"],
        ),
    )


def delete(creature_id):
    creature = data.get_one(creature_id)
    data.delete(creature)
