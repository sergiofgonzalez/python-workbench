"""A basic OAuth2 app implementing the password flow using FastAPI."""

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.status import HTTP_400_BAD_REQUEST

app = FastAPI()

fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice B. Cooper",
        "disabled": False,
        "hashed_password": "****", # replace with the password you'd like to use
    },
    "bob": {
        "username": "bob",
        "email": "bob@example.com",
        "full_name": "Bob C. Daniels",
        "disabled": True,
        "hashed_password": "****", # replace with the password you'd like to use
    },
}


class User(BaseModel):
    """A user model."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """Represents a user in the DB."""

    hashed_password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def fake_hash_password(password: str) -> str:
    """Simulates hashing a password."""
    return "fakehashed_" + password


def get_user_from_db(username: str) -> UserInDB | None:
    """Simulates retrieving a user from the db by username."""
    user_dict = fake_users_db.get(username)
    if user_dict:
        return UserInDB(**user_dict)  # ty:ignore[invalid-argument-type]
    return None


def fake_decode_token(token: str) -> dict[str, str]:
    """Decode the security token and return the associated user details within it."""
    # simplest strategy: in a real app, generate a JWT or similar
    username = token
    return {"username": username}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """Return the user associated to the token sent in the request."""
    user_details = fake_decode_token(token)
    user = get_user_from_db(user_details["username"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    user: Annotated[UserInDB, Depends(get_current_user)],
) -> UserInDB:
    """Return the current active user or raise exception if user disabled."""
    if user.disabled:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> dict[str, str]:
    """Path operation for the POST token endpoint."""
    user = get_user_from_db(form_data.username)
    if not user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    # simplest strategy: in a real app, generate a JWT or similar
    access_token = form_data.username
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
) -> User:
    """Path operation for the GET /users/me endpoint."""
    # it uses model filtering to prevent sending the hashed password in the response
    return current_user


@app.get("/items/")
async def read_items() -> dict[str, list[str]]:
    """Path operation for the GET /items/ endpoint."""
    return {"items": ["item1", "item2", "item3"]}
