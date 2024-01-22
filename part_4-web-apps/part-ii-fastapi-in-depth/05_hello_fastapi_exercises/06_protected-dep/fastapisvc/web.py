"""FastAPI app"""
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()


def authentication_check(authorization: Annotated[str | None, Header()] = None):
    if authorization is None or (
        authorization is not None
        and (
            not authorization.startswith("Bearer ")
            or len(authorization) <= len("Bearer ")
        )
    ):
        raise HTTPException(401)


@app.get("/public/hi")
def public_greet() -> str:
    return "Hello, world!"


@app.get("/protected/hi", dependencies=[Depends(authentication_check)])
def protected_greet() -> str:
    return "We salute you!"
