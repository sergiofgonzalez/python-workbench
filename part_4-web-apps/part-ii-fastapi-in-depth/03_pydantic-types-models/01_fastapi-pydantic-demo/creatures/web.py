"""Creatures service that exposes a single endpoint"""
from creatures.data import get_creatures
from fastapi import FastAPI
from creatures.model import Creature

app = FastAPI()


@app.get("/creatures")
def get_all() -> list[Creature]:
    return get_creatures()
