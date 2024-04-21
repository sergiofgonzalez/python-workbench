"""User Model Definitions"""

from pydantic import BaseModel


class User(BaseModel):
    name: str
    password_hash: str
