"""Illustrates the basics of FastAPI's background tasks."""

from datetime import UTC, datetime
from typing import Annotated

import aiofiles
from fastapi import BackgroundTasks, Depends, FastAPI

app = FastAPI()


async def write_log(message: str) -> None:
    """Simulates writing a log message to a file."""
    async with aiofiles.open("log.txt", "a") as log_file:
        now = datetime.now(UTC)
        await log_file.write(f"{now} | {message}\n")


async def get_query(
    background_tasks: BackgroundTasks,
    q: str | None = None,
) -> str | None:
    """Simulates a time-consuming query operation."""
    if q is not None:
        background_tasks.add_task(write_log, f"Query received: {q}")
    return q


@app.post("/send-notification/{username}")
async def send_notification(
    username: str,
    background_tasks: BackgroundTasks,
) -> dict[str, str]:
    """Path operation for sending a notification to a user."""
    background_tasks.add_task(write_log, f"Notification sent to {username}")
    return {
        "message": f"Hello, {username}!",
        "timestamp": datetime.now(UTC).isoformat(),
    }


@app.get("/items/{item_id}")
async def read_items(
    background_tasks: BackgroundTasks,
    item_id: str,
    q: Annotated[str | None, Depends(get_query)] = None,
) -> dict[str, str | None]:
    """Path operation for reading items with an optional query parameter."""
    background_tasks.add_task(write_log, f"Items read with query: {q}")
    return {"item": item_id, "query": q, "timestamp": datetime.now(UTC).isoformat()}
