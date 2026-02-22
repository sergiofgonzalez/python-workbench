"""A basic OAuth2 Password Bearer example."""

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    """Path operation for the GET /items/ endpoint."""
    return {"token": token}


class User(BaseModel):
    """Model for a User."""

    username: str
    email: EmailStr | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token: str) -> dict[str, str | bool | None]:
    """Simulates the decoding of the token."""
    print(f"Simulating the decoding of the token: {token}")
    return {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice B. Cooper",
        "disabled": False,
    }


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Return a User instance from the token."""
    user_dict = fake_decode_token(token)
    return User(
        user_dict["username"],
        user_dict["email"],
        user_dict["full_name"],
        user_dict["disabled"],
    )


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Path operation for GET /users/me."""
    return current_user

