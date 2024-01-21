"""Model specification for the creatures web app"""
from pydantic import BaseModel, constr, Field


class Creature(BaseModel):
    name: constr(min_length=1, to_upper=True) # type: ignore
    country: str
    area: str
    description: str = Field(..., min_length=2)
    aka: str
