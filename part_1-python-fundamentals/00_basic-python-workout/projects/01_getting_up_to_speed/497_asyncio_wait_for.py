"""Basic illustration of the usage of asyncio.wait_for."""

import asyncio

from rich import print  # noqa: A004


async def coro(delay: int, *, should_fail: bool = False) -> str:
    """Sleeps for `delay` seconds and fail if instructed."""
    task_name = asyncio.current_task().get_name()  # ty:ignore[possibly-missing-attribute]
    print(
        f">>> [cyan][{task_name}] delay={delay}, should_fail={should_fail}[/cyan]",
    )
    await asyncio.sleep(delay)
    if should_fail:
        msg = "Coroutine failed as requested."
        raise RuntimeError(msg)
    return f"Completed after {delay} seconds."


async def main() -> None:  # noqa: C901
    """Async application entry point."""
    # Scenario 1: coroutine completes before timeout
    try:
        result = await asyncio.wait_for(coro(2), timeout=3)
        print(f"Scenario 1: {result}")
    except TimeoutError:
        print("Scenario 1: The coroutine timed out.")
    else:
        print("Scenario 1: The coroutine completed successfully.")
    print("=" * 40)

    # Scenario 2: coroutine exceeds timeout
    try:
        result = await asyncio.wait_for(coro(5), timeout=3)
        print(f"Scenario 2: {result}")
    except TimeoutError:
        print("Scenario 2: The coroutine timed out.")
    else:
        print("Scenario 2: The coroutine completed successfully.")
    print("=" * 40)

    # Scenario 3: coroutine raises an exception before timeout
    try:
        result = await asyncio.wait_for(coro(2, should_fail=True), timeout=3)
        print(f"Scenario 3: {result}")
    except TimeoutError:
        print("Scenario 3: The coroutine timed out.")
    except RuntimeError as exc:
        print(f"Scenario 3: The coroutine raised an exception: {exc}")
    else:
        print("Scenario 3: The coroutine completed successfully.")
    print("=" * 40)

    # Scenario 4: checking cancellation behavior
    task = asyncio.create_task(coro(5))
    try:
        await asyncio.wait_for(task, timeout=2)
    except TimeoutError:
        print("Scenario 4: The coroutine timed out.")
        if task.cancelled():
            print("Scenario 4: The coroutine was cancelled.")
        else:
            print("Scenario 4: The coroutine was not cancelled and kept running.")
    else:
        print("Scenario 4: The coroutine completed successfully.")
    print("=" * 40)

if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
