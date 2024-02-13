"""Explorer resource web layer"""

from fastapi import APIRouter, HTTPException

import cryptid.service.explorer as service
from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.explorer import Explorer

router = APIRouter(prefix="/explorer")


@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()


@router.get("/{name}")
def get_one(name) -> Explorer:
    try:
        return service.get_one(name)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create(explorer: Explorer) -> Explorer:
    try:
        return service.create(explorer)
    except DuplicateError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.patch("/{name}")
def modify(name: str, explorer_dict: dict) -> Explorer:
    try:
        return service.modify(name, explorer_dict)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except DuplicateError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e


@router.put("/{name}")
def replace(name: str, explorer: Explorer) -> Explorer:
    try:
        return service.replace(name, explorer)
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
