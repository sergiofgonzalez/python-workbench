"""Greeter router: contains all path operations related to greetings."""

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Query, status

from app.routers.schemas import (
    GetScheduledOrderSchema,
    GetScheduledOrdersSchema,
    QueryScheduledOrdersSchema,
    ScheduledOrderSchema,
    ScheduledOrderStatusSchema,
)

router = APIRouter(prefix="/kitchen/schedules", tags=["kitchen/schedules"])


fake_schedules_db = {}


@router.get("/")
async def read_schedules(
    query: Annotated[QueryScheduledOrdersSchema, Query()],
) -> GetScheduledOrdersSchema:
    """Get a list of all orders scheduled for production."""
    schedules = list(fake_schedules_db.values())
    if query.progress:
        schedules = [
            schedule
            for schedule in schedules
            if schedule["status"] == ScheduledOrderStatusSchema.PROGRESS
        ]
    elif query.progress is False:
        schedules = [
            schedule
            for schedule in schedules
            if schedule["status"] != ScheduledOrderStatusSchema.PROGRESS
        ]
    if query.limit is not None:
        schedules = schedules[: query.limit]

    if query.since:
        schedules = [
            schedule
            for schedule in schedules
            if schedule["scheduled"] >= query.since
        ]
    return GetScheduledOrdersSchema(schedules=schedules)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_schedule(
    order: ScheduledOrderSchema,
) -> GetScheduledOrderSchema:
    """Schedule an order for production."""
    new_schedule_id = uuid4()
    new_schedule = GetScheduledOrderSchema(
        schedule_id=new_schedule_id,
        scheduled=datetime.now(UTC),
        status=ScheduledOrderStatusSchema.PROGRESS,
        order=order.order,
    )
    fake_schedules_db[new_schedule_id] = new_schedule.model_dump()
    return new_schedule


@router.get("/{schedule_id}")
async def read_schedule(schedule_id: UUID) -> GetScheduledOrderSchema:
    """Get an order scheduled for production by its ID."""
    schedule = fake_schedules_db.get(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled order not found",
        )
    return GetScheduledOrderSchema(**schedule)


@router.put("/{schedule_id}")
async def update_schedule(
    schedule_id: UUID,
    order: ScheduledOrderSchema,
) -> GetScheduledOrderSchema:
    """Update an order scheduled for production by its ID."""
    schedule = fake_schedules_db.get(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled order not found",
        )
    updated_schedule = GetScheduledOrderSchema(
        schedule_id=schedule_id,
        scheduled=schedule["scheduled"],
        status=schedule["status"],
        order=order.order,
    )
    fake_schedules_db[schedule_id] = updated_schedule.model_dump()
    return updated_schedule


@router.delete("/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule(schedule_id: UUID) -> None:
    """Delete an order scheduled for production by its ID."""
    if schedule_id not in fake_schedules_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled order not found",
        )
    del fake_schedules_db[schedule_id]


@router.get("/{schedule_id}/status")
async def read_schedule_status(schedule_id: UUID) -> ScheduledOrderStatusSchema:
    """Get the status of an order scheduled for production by its ID."""
    schedule = fake_schedules_db.get(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled order not found",
        )
    return ScheduledOrderStatusSchema(schedule["status"])


@router.post("/{schedule_id}/cancel")
async def cancel_schedule(schedule_id: UUID) -> GetScheduledOrderSchema:
    """Cancel an order scheduled for production by its ID."""
    schedule = fake_schedules_db.get(schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheduled order not found",
        )
    updated_schedule = GetScheduledOrderSchema(
        schedule_id=schedule_id,
        scheduled=schedule["scheduled"],
        status=ScheduledOrderStatusSchema.CANCELLED,
        order=schedule["order"],
    )
    fake_schedules_db[schedule_id] = updated_schedule.model_dump()
    return updated_schedule
