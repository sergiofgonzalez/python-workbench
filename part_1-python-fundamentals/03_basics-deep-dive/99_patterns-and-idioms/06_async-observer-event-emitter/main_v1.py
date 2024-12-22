"""Illustrate the Observer pattern implemented in Python."""

import asyncio


class NamedEvent(asyncio.Event):
    """Subclassed Event featuring a name."""

    def __init__(self, name: str) -> None:
        """Initialize NamedEvent instance."""
        if not name:
            msg = "a named event must have a name"
            raise ValueError(msg)
        self._name = name
        super().__init__()

    @property
    def name(self) -> str:
        """Return the name of the event."""
        return self._name


async def listener_1(event: NamedEvent) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_1: listener established, waiting for the event")
    await event.wait()
    print(f"listener_1: event {event.name} triggered: executing event logic")


async def listener_2(event: NamedEvent) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_2: listener established, waiting for the event")
    await event.wait()
    print(f"listener_2: event {event.name} triggered: executing event logic")


async def listener_3(event: NamedEvent) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_3: listener established, waiting for the event")
    await event.wait()
    print(f"listener_3: event {event.name} triggered: executing event logic")

async def listener_4(event: NamedEvent) -> None:
    """Actions to be performed when event is triggered."""
    print("listener_4: listener established, waiting for the event")
    await event.wait()
    print(f"listener_4: event {event.name} triggered: executing event logic")


async def main() -> None:
    """Application entry point."""
    quick_evt = NamedEvent("quick")
    slow_evt = NamedEvent("slow")
    never_evt = NamedEvent("never")

    # These are equivalent to on(event, cb)
    waiter_task_1 = asyncio.create_task(listener_1(quick_evt))
    waiter_task_2 = asyncio.create_task(listener_2(slow_evt))
    waiter_task_3 = asyncio.create_task(listener_3(quick_evt))
    waiter_task_4 = asyncio.create_task(listener_4(never_evt))  # noqa: F841, RUF006

    # sleep for 1/2 second and set the event2
    await asyncio.sleep(0.5)
    quick_evt.set()  # this is like emit, but without params

    # sleep for 1 second and set the event1
    await asyncio.sleep(1)
    slow_evt.set()  # this is like emit, but without params

    # wait until the waiter task is finished
    await asyncio.gather(waiter_task_1, waiter_task_2, waiter_task_3)


asyncio.run(main())
