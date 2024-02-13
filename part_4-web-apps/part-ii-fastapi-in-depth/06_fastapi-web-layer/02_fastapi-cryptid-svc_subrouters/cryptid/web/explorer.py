"""Explorer resource web layer"""

from fastapi import APIRouter

router = APIRouter(prefix="/explorer")


@router.get("/")
def top():
    return "root of explorer endpoint"
