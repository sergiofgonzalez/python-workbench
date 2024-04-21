"""Creature service layer"""

import os

from cryptid.model.creature import Creature

if os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.fake import creature as data
else:
    from cryptid.data import creature as data


def get_all() -> list[Creature]:
    return data.get_all()


def get_one(name: str) -> Creature:
    return data.get_one(name)


def create(creature: Creature) -> Creature:
    return data.create(creature)


def replace(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)


def modify(name: str, creature_dict: dict) -> Creature:
    patched_creature_dict = data.model_to_dict(data.get_one(name))
    for field in creature_dict.keys():
        patched_creature_dict[field] = creature_dict[field]

    return data.modify(
        name,
        Creature(
            name=patched_creature_dict["name"],
            country=patched_creature_dict["country"],
            description=patched_creature_dict["description"],
            aka=patched_creature_dict["aka"],
            area=patched_creature_dict["area"],
        ),
    )


def delete(name: str):
    creature = data.get_one(name)
    data.delete(creature)
