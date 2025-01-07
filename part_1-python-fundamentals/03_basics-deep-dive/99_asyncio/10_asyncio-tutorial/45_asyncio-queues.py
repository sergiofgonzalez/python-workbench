"""
Illustrate how to use asyncio queues to effectively distribute tasks across
workers.
"""

import asyncio
import random
import time


async def worker(name: str, queue: asyncio.Queue) -> None:
    """Worker template that process an item from the queue."""
    while True:
        # Get a work item from the queue
        sleep_seconds = await queue.get()

        # Do the work
        await asyncio.sleep(sleep_seconds)

        # Notify the queue the work is done
        queue.task_done()

        print(f"{name} is done: slept for {sleep_seconds:.3f} seconds")


async def main() -> None:
    """Async entry point."""
    # Create an asyncio queue to keep our work items
    queue = asyncio.Queue()

    # Generate work
    total_sleep_time = 0
    for _ in range(20):
        sleep_seconds = random.uniform(0.05, 1)
        total_sleep_time += sleep_seconds
        queue.put_nowait(sleep_seconds)

    # Create 3 workers to process the queue in parallel
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f"worker-{i}", queue))
        tasks.append(task)

    # Wait until queue is fully processed
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel worker tasks
    for task in tasks:
        task.cancel()

    # Wait until all worker tasks are cancelled, don't fail on exceptions
    await asyncio.gather(*tasks, return_exceptions=True)

    print("=" * 80)
    print(
        f"{len(tasks)} processed {total_sleep_time:.2f} seconds in {total_slept_for:.2f} seconds.",  # noqa: E501
    )


if __name__ == "__main__":
    asyncio.run(main())

