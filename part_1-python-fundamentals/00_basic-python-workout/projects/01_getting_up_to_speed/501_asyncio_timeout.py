"""Illustrates how to use asyncio.timeout to run asyncio.gather with a timeout."""

import asyncio


async def worker(name: str, delay: float) -> str:
    """Simulate a worker that takes some time to complete."""
    print(f"Worker {name} starting, will take {delay} seconds.")
    await asyncio.sleep(delay)
    return f"Worker {name} completed after {delay} seconds"


async def run_workers_with_timeout(timeout_after: float) -> None:
    """Run multiple workers with a timeout using asyncio.gather."""
    tasks = [
        asyncio.create_task(worker("A", 6), name="Worker A"),
        asyncio.create_task(worker("B", 7), name="Worker B"),
        asyncio.create_task(worker("C", 8), name="Worker C"),
    ]
    print(f"Running workers with a timeout of {timeout_after} seconds.")
    try:
        async with asyncio.timeout(timeout_after):
            results = await asyncio.gather(
                *tasks,
                return_exceptions=False,
            )
    except TimeoutError:
        print("One or more workers did not complete within the timeout period.")
        for task in tasks:
            if task.cancelled():
                print(f"{task.get_name()} was cancelled by async with.")
            elif not task.done():
                print(f"{task.get_name()} did not complete.")
            else:
                was_cancelled = task.cancel()
                print(f"{task.get_name()} was cancelled: {was_cancelled}")
    else:
        print("All workers completed within the timeout period.")
        for result in results:
            print(result)


async def main() -> None:
    """Async application entry point."""
    await run_workers_with_timeout(5)
    print("=" * 40)
    await run_workers_with_timeout(10)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
