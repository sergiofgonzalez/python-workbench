"""Explorer resource web layer"""

from fastapi import APIRouter

import cryptid.fake.explorer as service
from cryptid.model.explorer import Explorer
from cryptid.utils.log_config import get_logger

router = APIRouter(prefix="/explorer")


logger = get_logger(__name__)


@router.get("/")
def get_all() -> list[Explorer]:
    logger.debug("What the heck is that?")
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
