"""User service layer"""

import os
from datetime import datetime, timedelta

from jose import JWTError, jwt
from passlib.context import CryptContext

from cryptid.data.errors import MissingError
from cryptid.model.user import User
from cryptid.utils.log_config import get_logger

log = get_logger(__name__)

if os.getenv("CRYPTID_UNIT_TEST"):
    from cryptid.fake import user as data
else:
    from cryptid.data import user as data


SECRET_KEY = "some-secret-key-to-be-kept-secure"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def get_hash(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def get_jwt_username(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except JWTError:
        return None
    return username


def get_current_user(token: str) -> User | None:
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user
    return None


def lookup_user(username: str) -> User | None:
    try:
        return data.get_one(username)
    except MissingError as exc:
        log.error(exc)
        return None


def auth_user(name: str, plain: str) -> User | None:
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.password_hash):
        return None
    return user


def create_access_token(info: dict, expires: timedelta | None = None):
    src = info.copy()
    now = datetime.utcnow()
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_all() -> list[User]:
    return data.get_all()


def get_one(name: str) -> User:
    return data.get_one(name)


def create(user: User) -> User:
    return data.create(user)


def modify(name: str, user_dict: dict) -> User:
    patched_user_dict = data.model_to_dict(data.get_one(name))
    for field in user_dict.keys():
        patched_user_dict[field] = user_dict[field]
    return data.modify(
        name,
        User(
            name=patched_user_dict["name"],
            password_hash=patched_user_dict["password_hash"],
        ),
    )


def replace(name: str, user: User) -> User:
    return data.modify(name, user)


def delete(name: str) -> None:
    user = data.get_one(name)
    data.delete(user)
