"""Creature service layer"""

import fake.explorer as data
from cryptid.model.explorer import Explorer


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(explorer_id) -> Explorer | None:
    return data.get_one(explorer_id)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(explorer_id, explorer: Explorer) -> Explorer:
    return data.replace(explorer_id, explorer)


def modify(explorer_id, explorer: Explorer) -> Explorer:
    return data.modify(explorer_id, explorer)


def delete(explorer_id) -> bool:
    return data.delete(explorer_id)
