"""Illustrates how to use JWT and password hashes to a basic OAuth2 password flow."""

from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# JWT settings: key is generated using `openssl rand -hex 32`
# in a production app, this signing secret key wouldn't be hardcoded
JWT_SECRET_KEY = "****"  # noqa: S105
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

# this is a fake database, in production you would use a real database
# users have passwords "secret" and "tiger" respectively, hashed using Python pwdlib
# with argon2id and the recommended settings.
fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice B. Cooper",
        "disabled": False,
        "hashed_password": "****",  # replace with the hash of the password you'd like to use  # noqa: E501
    },
    "bob": {
        "username": "bob",
        "email": "bob@example.com",
        "full_name": "Bob C. Daniels",
        "disabled": True,
        "hashed_password": "****",  # replace with the hash of the password you'd like to use  # noqa: E501
    },
}


class Token(BaseModel):
    """Model for the /token response."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Model for the token data."""

    username: str | None = None


class User(BaseModel):
    """Model for the user."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """Model for the user in the database."""

    hashed_password: str


password_hash = PasswordHash.recommended()

# used to prevent timing attacks
DUMMY_PASSWORD_HASH = password_hash.hash("****")  # replace with the hash of a password you'd like to use

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return password_hash.hash(password)


def get_user(
    db: dict[str, dict[str, str | bool | None]],
    username: str | None,
) -> UserInDB | None:
    """Get a user from the database."""
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)  # ty:ignore[invalid-argument-type]
    return None


def authenticate_user(
    db: dict[str, dict[str, str | bool | None]],
    username: str,
    password: str,
) -> UserInDB | None:
    """Authenticate a user."""
    user = get_user(db, username)
    if not user:
        # to prevent timing attacks, password hash is verified even if the user
        # doesn't exist
        verify_password(password, DUMMY_PASSWORD_HASH)
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    data: dict[str, str | datetime],
    expires_delta_minutes: int | None,
) -> str:
    """Create a JWT access token."""
    data_to_encode = data.copy()
    if expires_delta_minutes:
        expire = datetime.now(UTC) + timedelta(minutes=expires_delta_minutes)
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt  # noqa: RET504


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Get the current user from the token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")  # ty:ignore[invalid-assignment]
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        raise credentials_exception from e
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """Get the current active user."""
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Path operation for the POST /token endpoint."""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = JWT_EXPIRATION_MINUTES
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta_minutes=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")  # noqa: S106


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Path operation for the GET /users/me endpoint."""
    return current_user


@app.get("/items/")
async def read_items() -> dict[str, list[str]]:
    """Path operation for the GET /items/ endpoint."""
    return {"items": ["item1", "item2", "item3"]}
