"""Illustrate the Observer pattern implemented in Python."""

import asyncio


async def listener_1(event: asyncio.Event) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_1: listener established, waiting for the event")
    await event.wait()
    print("listener_1: event triggered: executing event logic")


async def listener_2(event: asyncio.Event) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_2: listener established, waiting for the event")
    await event.wait()
    print("listener_2: event triggered: executing event logic")


async def listener_3(event: asyncio.Event) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_3: listener established, waiting for the event")
    await event.wait()
    print("listener_3: event triggered: executing event logic")


async def main() -> None:
    """Application entry point."""
    event_1 = asyncio.Event()
    event_2 = asyncio.Event()

    # These are equivalent to on(event, cb)
    waiter_task_1 = asyncio.create_task(listener_1(event_1))
    waiter_task_2 = asyncio.create_task(listener_2(event_1))
    waiter_task_3 = asyncio.create_task(listener_3(event_2))

    # sleep for 1/2 second and set the event2
    await asyncio.sleep(0.5)
    event_2.set()  # this is like emit, but without params

    # sleep for 1 second and set the event1
    await asyncio.sleep(1)
    event_1.set()  # this is like emit, but without params

    # wait until the waiter task is finished
    await asyncio.gather(waiter_task_1, waiter_task_2, waiter_task_3)


asyncio.run(main())
