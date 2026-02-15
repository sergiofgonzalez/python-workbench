"""Illustrates FastAPI support for other data types (datetimes, uuid, etc.)."""

from datetime import datetime, timedelta, date
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()



@app.put("/items/{item_id}")
async def update_item(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[datetime | None, Body()] = None,
) -> dict[str, date | datetime | timedelta | str | None]:
    """Path operation for updating an item."""
    start_process_dt = start_datetime + process_after
    duration = end_datetime - start_process_dt
    return {
        "item_id": str(item_id),
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process_datetime": start_process_dt,
        "duration": duration,
    }
