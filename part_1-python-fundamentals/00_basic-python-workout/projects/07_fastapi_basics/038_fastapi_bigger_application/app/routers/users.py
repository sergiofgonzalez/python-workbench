"""Users module in routers sub-package: user management path operations."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users() -> dict[str, list[str]]:
    """Path operation for the GET /users/ endpoint."""
    return {"user_ids": ["user1", "user2", "user3"]}


@router.get("/users/me", tags=["users"])
async def read_user_me() -> dict[str, str]:
    """Path operation for the GET /users/me endpoint."""
    return {"user_id": "the current user"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str) -> dict[str, str]:
    """Path operation for the GET /users/{username} endpoint."""
    return {"user_id": username}
