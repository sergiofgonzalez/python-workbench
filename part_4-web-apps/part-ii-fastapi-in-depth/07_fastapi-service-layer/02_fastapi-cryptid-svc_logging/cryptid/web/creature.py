"""Creature resource web layer"""

import cryptid.fake.creature as service
from fastapi import APIRouter
from cryptid.model.creature import Creature
from cryptid.utils.log_json import logger
import logging
router = APIRouter(prefix="/creature")


@router.get("/")
def get_all() -> list[Creature]:
    logger.info("Creatures everyhere!")
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature:
    return service.get_one(name)


@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)


@router.patch("/")
def modify(creature: Creature) -> Creature:
    return service.modify(creature)


@router.put("/")
def replace(creature: Creature) -> Creature:
    return service.replace(creature)


@router.delete("/{name}")
def delete(name) -> bool:
    return service.delete(name)
