"""Creature resource web layer"""

from fastapi import APIRouter, HTTPException, status

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.creature import Creature
from cryptid.service import creature as service

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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(creature: Creature) -> Creature:
    try:
        return service.create(creature)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e


@router.patch("/{name}")
def modify(name: str, creature_dict: dict) -> Creature:
    try:
        return service.modify(name, creature_dict)
    except MissingError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e


@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature:
    try:
        return service.replace(name, creature)
    except MissingError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e


@router.delete("/{name}", status_code=204)
def delete(name):
    try:
        service.delete(name)
    except MissingError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
