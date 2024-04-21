"""Explorer Model Definitions"""

from pydantic import BaseModel


class Explorer(BaseModel):
    name: str
    country: str
    description: str
