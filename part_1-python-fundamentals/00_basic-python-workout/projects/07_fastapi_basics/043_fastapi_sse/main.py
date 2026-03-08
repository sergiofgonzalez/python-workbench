"""Illustrates the basics of FastAPI Server-Sent Events (SSE)."""

from collections.abc import AsyncIterable, Iterable
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.sse import EventSourceResponse, ServerSentEvent
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """Represents an item."""

    name: str
    price: float


items = [
    Item(name="Item 1", price=10.0),
    Item(name="Item 2", price=20.0),
    Item(name="Item 3", price=30.0),
]


@app.get("/items/stream", response_class=EventSourceResponse)
async def stream_items() -> AsyncIterable[Item]:
    """Path operation for streaming items."""
    for item in items:
        yield item


@app.get("/items/stream-no-async", response_class=EventSourceResponse)
def stream_items_no_async() -> Iterable[Item]:
    """Path operation for streaming items without async."""
    yield from items


@app.get("/items/stream-events", response_class=EventSourceResponse)
async def stream_items_on_events() -> AsyncIterable[Item]:
    """Path operation for streaming items on events."""
    yield ServerSentEvent(comment="Starting stream of item updates")
    for index, item in enumerate(items):
        yield ServerSentEvent(
            data=item,
            event="item update",
            id=str(index + 1),
            retry=5000,
        )


@app.get("/items/stream-logs", response_class=EventSourceResponse)
async def stream_raw_log_lines() -> AsyncIterable[ServerSentEvent]:
    """Path operation for streaming raw log lines."""
    log_lines = [
        "2024-06-01 12:00:00 INFO Starting server",
        "2024-06-01 12:01:00 INFO Received request for /items/stream",
        "2024-06-01 12:02:00 INFO Sent item updates to client",
    ]
    for line in log_lines:
        yield ServerSentEvent(raw_data=line)


@app.get("/items/stream-resume", response_class=EventSourceResponse)
async def stream_items_with_resume(
    last_event_id: Annotated[str | None, Header()] = None,
) -> AsyncIterable[Item]:
    """Path operation for streaming items with resume support."""
    start_index = int(last_event_id) if last_event_id is not None else 0
    for item in items[start_index:]:
        yield item


class Prompt(BaseModel):
    """Represents a prompt for generating items."""

    text: str


@app.post("/chat/stream", response_class=EventSourceResponse)
async def stream_chat_responses(prompt: Prompt) -> AsyncIterable[str]:
    """Path operation for streaming chat responses based on a prompt."""
    for word in prompt.text.split():
        yield ServerSentEvent(data=word, event="token")
    yield ServerSentEvent(raw_data="[DONE]", event="done")
