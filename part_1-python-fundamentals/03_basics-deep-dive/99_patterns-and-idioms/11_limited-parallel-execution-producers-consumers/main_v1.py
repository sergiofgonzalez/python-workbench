"""Illustrates how to do limited parallel execution with TaskQueue."""

import asyncio
import random
import time

from work_queue import WorkQueue


def sleep_fn(seconds: float) -> None:
    """Return a function that features an async sleep for the given seconds.

    The return of this function is a coroutine function that will be used as a work item
    in the work queue.
    """

    async def fn() -> None:
        await asyncio.sleep(seconds)

    return fn


async def main() -> None:
    """Async application entry point."""
    work_queue = WorkQueue(concurrency=3)

    start_ts = time.perf_counter()
    total_seconds_to_sleep = 0
    for _ in range(20):
        seconds_to_sleep = random.uniform(0.05, 1)  # noqa: S311
        total_seconds_to_sleep += seconds_to_sleep
        work_queue.put_work_item(sleep_fn(seconds_to_sleep))

    # all work done, now run to completion
    await work_queue.until_all_work_done()
    real_wait_time = time.perf_counter() - start_ts
    print(
        f"Processed {total_seconds_to_sleep:.3f} seconds "
        f"in {real_wait_time:.3f} seconds",
    )


if __name__ == "__main__":
    asyncio.run(main())
