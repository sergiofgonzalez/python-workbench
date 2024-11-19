"""
Illustrates the use of asyncio.to_thread() to run blocking calls in the event
loop.
"""

import asyncio
import time

from rich import print

colors = {}


async def long_running_task(
    *,
    num_steps: int = 5,
    delay_step: float = 0.5,
) -> None:
    """
    Simulate a long running task that is prepared to progress cooperatively
    in the event loop by yielding control to the event loop while in progress.
    """
    start = time.perf_counter()
    t = asyncio.current_task()
    color_idx = 8 + len(colors)
    colors[t.get_name()] = 8 + color_idx
    print(f"[yellow]>>>{t.get_name()} has started executing")
    for i in range(1, num_steps + 1):
        progress_bar = "#" * i
        print(f"[color({color_idx})]{t.get_name()}: {progress_bar}")
        # Simulate some I/O and release control of the event loop
        await asyncio.sleep(delay_step)

    print(
        f"[yellow]>>>{t.get_name()} took {time.perf_counter() - start:.3f} seconds to complete",  # noqa: COM812
    )


def blocking_call(num_steps: int = 5, delay_step: float = 0.5) -> None:
    """Simulate a blocking task."""
    start = time.perf_counter()
    color_idx = 8 + len(colors)
    colors["blocking_task"] = 8 + color_idx
    print("[yellow]>>>blocking_task has started executing")
    for i in range(1, num_steps + 1):
        progress_bar = "#" * i
        print(f"[color({color_idx})]blocking_task: {progress_bar}")
        # Simulate some blocking I/O
        time.sleep(delay_step)

    print(
        f"[yellow]>>>blocking_task took {time.perf_counter() - start:.3f} seconds to complete",  # noqa: COM812
    )


async def wrapped_blocking_call() -> None:
    """Wrap a blocking call as a coroutine."""
    blocking_call(num_steps=5)


async def main() -> None:
    """Async entry point."""
    # Checking that without blocking the event loop, all tasks cooperate to
    # finalization
    # async with asyncio.TaskGroup() as group:
    #     for i in range(5):
    #         group.create_task(long_running_task(num_steps=5), name=f"Task_{i}")

    # Now we introduced a blocking call
    # print("=" * 80)
    # async with asyncio.TaskGroup() as group:
    #     for i in range(5):
    #         group.create_task(long_running_task(num_steps=5), name=f"Task_{i}")

    #     group.create_task(wrapped_blocking_call())

    # Now we use to_thread to run the blocking I/O in a separate thread
    # Note how the slowness of the blocking call does not affect the
    # well-behaved tasks
    print("=" * 80)
    async with asyncio.TaskGroup() as group:
        for i in range(5):
            group.create_task(long_running_task(num_steps=5), name=f"Task_{i}")

        coro = asyncio.to_thread(blocking_call, num_steps=10, delay_step=0.75)
        group.create_task(coro)

    print("Done with both sync and async tasks in the event loop")

if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
