"""Creature resource web layer"""

from fastapi import APIRouter, HTTPException

import cryptid.service.creature as service
from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.creature import Creature

router = APIRouter(prefix="/creature")


@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Creature:
    try:
        return service.get_one(name)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except DuplicateError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.patch("/{name}")
def modify(name: str, creature_dict: dict) -> Creature:
    try:
        return service.modify(name, creature_dict)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except DuplicateError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature:
    try:
        return service.replace(name, creature)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except DuplicateError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.delete("/{name}", status_code=204)
def delete(name):
    try:
        service.delete(name)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
