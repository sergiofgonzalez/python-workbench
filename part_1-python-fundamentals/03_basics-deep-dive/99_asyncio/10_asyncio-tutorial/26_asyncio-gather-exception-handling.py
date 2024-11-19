"""Illustrates how to deal with exceptions when using asyncio.gather()."""

import asyncio
import time

from rich import print


async def async_that_raises() -> None:
    """Simulate an async operation that raise an exception."""
    print("[red] This will raise in 2 seconds [/red]")
    await asyncio.sleep(2)
    error_message = "Operation failed!"
    raise RuntimeError(error_message)


async def async_that_returns() -> str:
    """Simulate an async operation that returns a value."""
    print("[green] This will complete after 3 seconds [/green]")
    await asyncio.sleep(3)
    print("[green] Done! [/green]")
    return "Successfully completed!"


async def run_gather_swallowing_exceptions() -> None:
    """Run coroutines concurrently telling gather() to swallow exceptions."""
    start = time.perf_counter()

    results = await asyncio.gather(
        async_that_returns(),
        async_that_raises(),
        return_exceptions=True,
    )
    end = time.perf_counter()
    print(f"Process took: {end - start:0.2f} seconds.")

    # Iterating over the results
    for i, result in enumerate(results):
        print(f"{i}: {result} ({type(result)})")


async def run_gather_default_exception_handling() -> None:
    """Run coroutines concurrently gather() (default exception handling)."""
    start = time.perf_counter()

    try:
        results = await asyncio.gather(
            async_that_returns(),
            async_that_raises(),
        )
        for i, result in enumerate(results):
            print(f"{i}: {result} ({type(result)})")
    except RuntimeError as e:
        print(f"[blue] Whole process failed: results unavailable: {e} [/blue]")
    end = time.perf_counter()
    print(f"Process took: {end - start:0.2f} seconds.")


async def run_gather_default_exception_handling_awaiting() -> None:
    """
    Run coroutines concurrently gather() (default exception handling with
    explicit await for other running tasks).
    """
    start = time.perf_counter()
    tasks = [
        asyncio.create_task(async_that_raises()),
        asyncio.create_task(async_that_returns()),
    ]
    try:
        results = await asyncio.gather(*tasks)
        for i, result in enumerate(results):
            print(f"{i}: {result} ({type(result)})")
    except RuntimeError as e:
        print(f"[blue] Whole process failed: results unavailable: {e} [/blue]")
        # Dealing with running tasks that might or might not have failed
        for task in tasks:
            if not task.done():
                try:
                    result = await task
                    print(f"Individual task completed: {result}")
                except Exception as e:  # noqa: BLE001
                    print(f"Failed task was already handled: {e}")
    end = time.perf_counter()
    print(f"Process took: {end - start:0.2f} seconds.")


async def main() -> None:
    """Entry point of the app."""
    # print("--- swallowing exceptions")
    # await run_gather_swallowing_exceptions()
    # print("--- default mode")
    # await run_gather_default_exception_handling()
    print("--- default mode with explicit task waiting")
    await run_gather_default_exception_handling_awaiting()

if __name__ == "__main__":
    asyncio.run(main())
