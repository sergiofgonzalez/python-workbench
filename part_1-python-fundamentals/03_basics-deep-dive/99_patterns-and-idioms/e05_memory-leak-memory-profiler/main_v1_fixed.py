"""Illustrate how to identify an event related memory leak in Python."""

import asyncio
import random
import sys
import time

from events import EventEmitter

FIFTY_MILLISECONDS = 0.050
RUNNING_TIME_2_MINS = 2 * 60


async def register_leaky_events(
    event_emitter: EventEmitter,
    listeners: list[callable],
) -> None:
    """Register an event that will be never triggered to create a memory leak."""

    def evt_handler_fn(big_ass_str: str) -> None:
        def fn() -> None:
            return print(big_ass_str)

        return fn

    while True:
        big_ass_str = random.randbytes(1_000_000).hex()  # noqa: S311
        evt_handler = evt_handler_fn(big_ass_str)
        event_emitter.register_listener("evt_that_never_was", evt_handler)
        listeners.append(evt_handler)
        await asyncio.sleep(FIFTY_MILLISECONDS)


async def stop_after_duration_expires() -> None:
    """Stop program after a given duration."""
    start = time.perf_counter()
    running_time = time.perf_counter() - start
    while running_time <= RUNNING_TIME_2_MINS:  # noqa: ASYNC110
        await asyncio.sleep(1)
        if int(running_time) % 15 == 0:
            print(f">> {int(running_time)}/{RUNNING_TIME_2_MINS} seconds elapsed")
        running_time = time.perf_counter() - start
    print("Running time expired!")
    sys.exit(0)


async def unregister_leaky_events(
    event_emitter: EventEmitter,
    listeners: list[callable],
) -> None:
    """Unregister leaky events after some time."""
    await asyncio.sleep(30)
    print(">> elapsed 30 secs: removing listeners")
    while True:
        listener = listeners.pop(0)
        event_emitter.remove_listener("evt_that_never_was", listener)
        await asyncio.sleep(FIFTY_MILLISECONDS)


async def main() -> None:
    """Application entry point."""
    event_emitter = EventEmitter()
    listeners = []
    asyncio.create_task(stop_after_duration_expires())  # noqa: RUF006
    await asyncio.gather(
        register_leaky_events(event_emitter, listeners),
        unregister_leaky_events(event_emitter, listeners),
    )


if __name__ == "__main__":
    asyncio.run(main())
