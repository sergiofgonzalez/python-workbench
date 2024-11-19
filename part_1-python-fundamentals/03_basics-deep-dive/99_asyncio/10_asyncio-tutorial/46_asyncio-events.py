"""Using events to notify multiple tasks that some event has happened."""

import asyncio
import time


async def event_handler(event: asyncio.Event) -> None:
    """Handle the event when fired."""
    started_at = time.perf_counter()
    # block until the event is fired
    await event.wait()
    print(f"Got event: waited for {time.perf_counter() - started_at:.3f} sec.")


async def trigger_event_after(event: asyncio.Event, delay: float) -> None:
    """Trigger an event after some delay."""
    await asyncio.sleep(delay)
    event.set()


async def main() -> None:
    """Async entry point."""
    # Create Event object
    hello_event = asyncio.Event()
    done_event = asyncio.Event()
    some_other_event_no_one_cares = asyncio.Event()

    # Create a couple of tasks for the event
    handlers = [
        asyncio.create_task(event_handler(hello_event)),
        asyncio.create_task(event_handler(done_event)),
    ]

    await asyncio.gather(
        trigger_event_after(hello_event, 1),
        trigger_event_after(some_other_event_no_one_cares, 2),
        trigger_event_after(done_event, 3),
    )

    await asyncio.gather(*handlers)


if __name__ == "__main__":
    asyncio.run(main())
