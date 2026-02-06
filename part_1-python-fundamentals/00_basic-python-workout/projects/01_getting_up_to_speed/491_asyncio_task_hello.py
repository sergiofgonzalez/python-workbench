"""Illustrates the basics of asyncio tasks."""

import asyncio
import random

from rich import print  # noqa: A004


async def randint_async(max_sleep: int = 3) -> int:
    """Asynchronously sleep for a random duration up to max_sleep seconds."""
    sleep_time = random.randint(0, max_sleep)  # noqa: S311
    print(f"[yellow]Sleeping for {sleep_time} seconds...[/yellow]")
    await asyncio.sleep(sleep_time)
    print(f"[yellow]Slept for {sleep_time} seconds.[/yellow]")
    return sleep_time


async def randint_async_fail(max_sleep: int = 3) -> int:
    """Asynchronously sleep for a random duration up to max_sleep seconds, then raise an exception."""  # noqa: E501
    sleep_time = random.randint(0, max_sleep)  # noqa: S311
    print(f"[red]Sleeping for {sleep_time} seconds...[/red]")
    await asyncio.sleep(sleep_time)
    msg = "Intentional failure after sleep"
    raise RuntimeError(msg)


async def main() -> None:
    """Async application entry point."""
    # Task that completes successfully
    task = asyncio.create_task(randint_async())
    print(f"Created task: {task.get_name()}")
    if not task.done():
        print("Task is still running...")
    result = await task
    print(f"Task {task.get_name()} completed with result: {result}")
    print("=" * 40)

    # Task that raises an exception
    failing_task = asyncio.create_task(randint_async_fail())
    print(f"Created failing task: {failing_task.get_name()}")
    if not failing_task.done():
        print("Failing task is still running...")
    try:
        await failing_task
    except RuntimeError as exc:
        print(f"Caught an exception from task {failing_task.get_name()}: {exc}")

    # if you don't know if it may fail, you can check:
    if failing_task.done():
        if failing_task.exception() is not None:
            print(
                f"Task {failing_task.get_name()} failed with exception: "
                f"{failing_task.exception()}",
            )
        else:
            print(
                f"Task {failing_task.get_name()} completed successfully with result: "
                f"{failing_task.result()}",
            )


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
