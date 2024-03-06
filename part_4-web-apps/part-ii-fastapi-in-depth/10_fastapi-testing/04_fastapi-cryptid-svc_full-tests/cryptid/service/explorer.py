"""Explorer service layer"""

import os

from cryptid.model.explorer import Explorer

if os.getenv("CRYPTID_UNIT_TEST"):
    import cryptid.fake.explorer as data
else:
    import cryptid.data.explorer as data


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(name: str, explorer: Explorer) -> Explorer:
    return data.modify(name, explorer)


def modify(name: str, explorer_dict: dict) -> Explorer:
    patched_explorer_dict = data.model_to_dict(data.get_one(name))
    for field in explorer_dict.keys():
        patched_explorer_dict[field] = explorer_dict[field]

    return data.modify(
        name,
        Explorer(
            name=patched_explorer_dict["name"],
            country=patched_explorer_dict["country"],
            description=patched_explorer_dict["description"],
        ),
    )


def delete(name: str):
    explorer = data.get_one(name)
    data.delete(explorer)
