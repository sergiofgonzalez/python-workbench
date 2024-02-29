"""User resource web layer"""

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from cryptid.data.errors import DuplicateError, MissingError
from cryptid.model.user import User
from cryptid.service import user as service

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")

# This dependency makes a post to "/user/token" from
# a form containing a username and password and returns
# an access token
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthenticated():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrent username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# This endpoint will be referenced to by any call that has the oauth2_dep
# dependency
@router.post("/token")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        return unauthenticated()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(
        info={"sub": user.name}, expires=expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    return {"token": token}


@router.get("")
@router.get("/")
def get_all() -> list[User]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> User:
    try:
        return service.get_one(name)
    except MissingError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e


@router.post("", status_code=status.HTTP_201_CREATED)
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: User) -> User:
    try:
        return service.create(user)
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e


@router.patch("/{name}")
def modify(name: str, user_dict: dict) -> User:
    try:
        return service.modify(name, user_dict)
    except MissingError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e


@router.put("/{name}")
def replace(name: str, user: User) -> User:
    try:
        return service.replace(name, user)
    except MissingError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        ) from e
    except DuplicateError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(e)
        ) from e


@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        service.delete(name)
    except MissingError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
