"""Illustrates how to get the current and running tasks."""

import asyncio
from datetime import UTC, datetime


async def long_running_task(iter_delay: int) -> None:
    """Infinite async loop."""
    while True:
        # yield control of the event loop so that other task can cooperate
        print(f"About to wait for {iter_delay} seconds.")
        await asyncio.sleep(iter_delay)


async def main() -> None:
    """App entry point."""
    task1 = asyncio.create_task(long_running_task(iter_delay=2), name="Task #1")  # noqa: F841, RUF006
    task2 = asyncio.create_task(long_running_task(iter_delay=3), name="Task #2")  # noqa: F841, RUF006

    while True:
        task = asyncio.current_task()
        tasks = asyncio.all_tasks()
        task_names = [task.get_name() for task in tasks]
        now = datetime.now(UTC)
        print("Press CTRL+C to quit")
        print(
            f"{now}: {task.get_name()} ({task.get_coro().__name__}) is the current task from tasks: {task_names}",  # noqa: E501
        )
        await asyncio.sleep(1)


if __name__ == "__main__":
    # Start the event loop in the current thread
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("User requested termination.")
