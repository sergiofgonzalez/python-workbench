"""Explorer resource web layer"""

import fake.explorer as service
from fastapi import APIRouter
from model.explorer import Explorer

router = APIRouter(prefix="/explorer")


@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Explorer:
    return service.get_one(name)


@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)


@router.patch("/")
def modify(explorer: Explorer) -> Explorer:
    return service.modify(explorer)


@router.put("/")
def replace(explorer: Explorer) -> Explorer:
    return service.replace(explorer)


@router.delete("/{name}")
def delete(name) -> bool:
    return service.delete(name)
