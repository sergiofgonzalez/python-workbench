"""A simple FastAPI app illustrating custom dependencies"""
from fastapi import Depends, FastAPI

app = FastAPI()


def user_dep(name: str, password: str):
    return {"name": name, "valid": True}


def check_user_dep(name: str):
    if name.lower() != "jason":
        raise ValueError(
            "name expected to be 'jason'"
        )


@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:
    # alternative syntax
    # def get_user(user: user_dep = Depends()) -> dict:
    return user


@app.get("/v2/user")
def get_user_v2(user: user_dep = Depends()) -> dict:
    return user


@app.get("/user/check", dependencies=[Depends(check_user_dep)])
def check_user() -> bool:
    return True
