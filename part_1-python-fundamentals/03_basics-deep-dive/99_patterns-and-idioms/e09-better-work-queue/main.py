"""Using WorkQueue to classify a large list of numbers into even and odd."""

import asyncio
import time

from workqueue_v2 import WorkQueue

even_nums = []
odd_nums = []


def classify_fn(num: int) -> None:
    """Return the work_item coroutine."""

    async def fn() -> None:
        if num % 2 == 0:
            even_nums.append(num)
        else:
            odd_nums.append(num)

    return fn


async def classify_even_odd_numbers(
    num_count: int,
    concurrency: int = 2,
) -> tuple[list[int], list[int]]:
    """Classify a large list of numbers into even and odd asynchronously."""
    # Create the work queue
    work_queue = WorkQueue(concurrency)

    # Start pushing work items in the work queue
    for i in range(num_count):
        await work_queue.run_work(classify_fn(i))
        if i % 100 == 0:
            print(f">>> {i} numbers produced")

    await work_queue.until_work_done()
    print("All done!")


async def main() -> None:
    """Async application entry point."""
    start = time.perf_counter()
    await classify_even_odd_numbers(1_000_000, concurrency=3)
    print(f"Process took {time.perf_counter() - start:.6f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
