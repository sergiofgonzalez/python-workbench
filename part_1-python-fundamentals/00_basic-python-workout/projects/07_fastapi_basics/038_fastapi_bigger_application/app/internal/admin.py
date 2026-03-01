"""admin module in internal sub-package: admin-related functionality."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/")
async def admin_action() -> dict[str, str]:
    """Path operation for the POST /admin/ endpoint."""
    return {"message": "Admin action performed successfully!"}
