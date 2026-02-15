"""Illustrates the basics of FastAPI response models."""

from typing import Any, Union

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    """Defines the data model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """Path operation for creating an item."""
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    """Path operation for reading items."""
    return [
        Item(name="foo", price=1.23),
        Item(name="bar", description="baz", price=3.21, tax=1.11),
    ]


@app.post("/v2/items/", response_model=Item)
async def create_item_v2(item: Item) -> Any:  # noqa: ANN401
    """Path operation for creating an item."""
    return item


@app.get("/v2/items/", response_model=list[Item])
async def read_items_v2() -> Any:  # noqa: ANN401
    """Path operation for reading items."""
    return [
        Item(name="foo", price=1.23),
        Item(name="bar", description="baz", price=3.21, tax=1.11),
    ]


class UserIn(BaseModel):
    """Defines the data model for a user input."""

    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    """Path operation for creating a user."""
    return user


class UserInV2(BaseModel):
    """Defines the data model for a user input."""

    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    """Defines the data model for a user output."""

    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/v2/user/")
async def create_user_v2(user: UserInV2) -> UserOut:
    """Path operation for creating a user."""
    return user  # ty:ignore[invalid-return-type]


class BaseUser(BaseModel):
    """Defines the base data model for a user."""

    username: str
    email: EmailStr
    full_name: str | None = None


class UserInV3(BaseUser):
    """Defines the data model for a user input."""

    password: str


@app.post("/v3/user/")
async def create_user_v3(user: UserInV3) -> BaseUser:
    """Path operation for creating a user."""
    return user


@app.get("/portal")
async def read_portal(*, teleport: bool = False) -> Response:
    """Path operation for reading the portal."""
    if teleport:
        return RedirectResponse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Welcome to the portal!"})


@app.get("/teleport")
async def teleport() -> RedirectResponse:
    """Path operation for teleporting."""
    return RedirectResponse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


# This one generates a fastapi.exceptions.FastAPIError: "Invalid args for response Field!"  # noqa: E501
# @app.get("/portal2")
# async def read_portal2(*, teleport: bool = False) -> Response | dict[str, str]:
#     """Path operation for reading the portal."""
#     if teleport:
#         return RedirectResponse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # noqa: E501, ERA001
#     return {"message": "Welcome to the portal!"}  # noqa: ERA001


@app.get("/portal2", response_model=None)
async def read_portal2(*, teleport: bool = False) -> Response | dict[str, str]:
    """Path operation for reading the portal."""
    if teleport:
        return RedirectResponse("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Welcome to the portal!"}


class ItemV2(BaseModel):
    """Defines the data model for an item."""

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}")
async def read_item(item_id: str) -> ItemV2:
    """Path operation for reading an item."""
    return items[item_id]


@app.get("/v2/items/{item_id}", response_model_exclude_unset=True)
async def read_item_v2(item_id: str) -> ItemV2:
    """Path operation for reading an item."""
    return items[item_id]


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get("/items/{item_id}/name", response_model_include={"name", "description"})
async def read_item_name(item_id: str) -> Item:
    """Path operation for reading an item name."""
    return items[item_id]


@app.get("/items/{item_id}/public", response_model_exclude={"tax"})
async def read_item_public(item_id: str) -> Item:
    """Path operation for reading an item's public information."""
    return items[item_id]


class ItemBase(BaseModel):
    """Defines the base data model for an item."""

    name: str
    description: str | None = None


class ItemPublic(ItemBase):
    """Defines the data model for a public item."""

    price: float
    tags: list[str] = []


@app.get("/v2/items/{item_id}/name")
async def read_item_name_v2(item_id: str) -> ItemBase:
    """Path operation for reading an item name."""
    return items[item_id]


@app.get("/v2/items/{item_id}/public")
async def read_item_public_v2(item_id: str) -> ItemPublic:
    """Path operation for reading an item's public information."""
    return items[item_id]


class UserInV4(BaseModel):
    """Defines the data model for a user input."""

    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOutV4(BaseModel):
    """Defines the data model for a user output."""

    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDBV4(BaseModel):
    """Defines the data model for a user in the database."""

    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str) -> str:
    """Fake password hasher."""
    return "supersecret" + raw_password


def fake_save_user(user_in: UserInV4) -> UserInDBV4:
    """Fake save user."""
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDBV4(**user_in.model_dump(), hashed_password=hashed_password)
    return user_in_db  # noqa: RET504


@app.post("/v4/user/")
async def create_user_v4(user: UserInV4) -> UserOutV4:
    """Path operation for creating a user."""
    user_in_db = fake_save_user(user)
    return UserOutV4(**user_in_db.model_dump())


class BaseUserV5(BaseModel):
    """Defines the data model for base user."""

    username: str
    email: EmailStr
    full_name: str | None = None


class UserInV5(BaseUserV5):
    """Defines the data model for a user input."""

    password: str


class UserInDBV5(BaseUserV5):
    """Defines the data model for a user in the database."""

    hashed_password: str


@app.post("/v5/user/")
async def create_user_v5(user: UserInV5) -> BaseUserV5:
    """Path operation for creating a user."""
    user_in_db = fake_save_user(user)
    return user_in_db  # noqa: RET504


class BaseItem(BaseModel):
    """Defines the data model for a base item."""

    description: str
    type: str


class CarItem(BaseItem):
    """Defines the data model for a car item."""

    type: str = "car"


class PlaneItem(BaseItem):
    """Defines the data model for a plane item."""

    type: str = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/v3/items/{item_id}", response_model=Union[CarItem, PlaneItem])  # noqa: UP007
async def read_item_v3(item_id: str) -> Any:  # noqa: ANN401
    """Path operation for reading an item."""
    return items[item_id]


@app.get("/v4/items/{item_id}")
async def read_item_v4(item_id: str) -> PlaneItem | CarItem:
    """Path operation for reading an item."""
    return items[item_id]


class ItemV3(BaseModel):
    """Defines the data model for a base item."""

    description: str
    name: str


items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/v3/items/", response_model=list[ItemV3])
async def read_items_v3() -> Any:  # noqa: ANN401
    """Path operation for reading items."""
    return items


@app.get("/v4/items/")
async def read_items_v4() -> list[ItemV3]:
    """Path operation for reading items."""
    return items


@app.get("/keyword-heights/", response_model=dict[str, float])
async def read_keyword_heights() -> Any:  # noqa: ANN401
    """Path operation for reading keyword heights."""
    return {"foo": 1.23, "bar": 3.21}


@app.get("/v2/keyword-heights/")
async def read_keyword_heights_v2() -> dict[str, float]:
    """Path operation for reading keyword heights."""
    return {"foo": 1.23, "bar": 3.21}
