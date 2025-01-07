"""Illustrate how you can get individual results from PCLimit."""

import asyncio
import random
import time

from pclimit import PCLimit


async def async_work() -> float:
    """Async piece of work to be handled by run()."""
    delay_seconds = random.uniform(0.5, 1.5)  # noqa: S311
    await asyncio.sleep(delay_seconds)
    return delay_seconds


async def main() -> None:
    """Async application entry point."""
    futures = []
    start = time.perf_counter()
    async with PCLimit(concurrency=3) as pclimit:
        for _ in range(10):
            future_sleep = await pclimit.run(async_work)
            futures.append(future_sleep)
        # values are not available yet, they're in "Pending" status
        print(futures)

    # once you're outside the block, the futures will be available
    total_sleep = time.perf_counter() - start
    total_requested_sleep = 0
    for future in futures:
        print(f"{future.result():.3f}")
        total_requested_sleep += future.result()

    print(f"Total requested sleep: {total_requested_sleep:.3f} seconds.")
    print(f"Actual sleep: {total_sleep:.3f} seconds.")
    print(f"compression: {total_sleep / total_requested_sleep:.3f}")


if __name__ == "__main__":
    asyncio.run(main())
