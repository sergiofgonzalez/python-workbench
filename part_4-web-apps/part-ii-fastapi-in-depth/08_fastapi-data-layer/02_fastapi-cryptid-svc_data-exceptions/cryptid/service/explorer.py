"""Explorer service layer"""

import cryptid.data.explorer as data
from cryptid.model.explorer import Explorer


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(explorer_id) -> Explorer:
    return data.get_one(explorer_id)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(explorer_id: str, explorer: Explorer) -> Explorer:
    return data.modify(explorer_id, explorer)


def modify(explorer_id: str, explorer_dict: dict) -> Explorer:
    patched_explorer_dict = data.model_to_dict(data.get_one(explorer_id))
    for field in explorer_dict.keys():
        patched_explorer_dict[field] = explorer_dict[field]

    return data.modify(
        explorer_id,
        Explorer(
            name=patched_explorer_dict["name"],
            country=patched_explorer_dict["country"],
            description=patched_explorer_dict["description"],
        ),
    )


def delete(explorer_id: str):
    explorer = data.get_one(explorer_id)
    data.delete(explorer)
