"""Limited parallel execution using producers/consumers."""

import asyncio
import random
import time


async def consumer(name: str, queue: asyncio.Queue) -> None:
    """Consumer template."""
    while True:
        # Get a work item from the queue if available, else sleep
        work_item = await queue.get()

        # Process the work item
        num_seconds = await work_item()

        # Notify the queue that the work is done
        queue.task_done()

        print(f"{name} is done: slept for {num_seconds:.3f} seconds")


def delay_fn(seconds: float) -> float:
    """Work processing coroutine."""

    async def fn() -> float:
        await asyncio.sleep(seconds)
        return seconds

    return fn


async def main() -> None:
    """Async entry point."""
    # Create the work queue
    queue = asyncio.Queue()

    # Generate some work
    total_sleep_time = 0
    for _ in range(20):
        sleep_seconds = random.uniform(0.05, 1)  # noqa: S311
        total_sleep_time += sleep_seconds
        queue.put_nowait(delay_fn(sleep_seconds))

    # Create 3 workers to process the queue
    # (limited parallel execution with concurrency = 3)
    tasks = []
    for i in range(5):
        task = asyncio.create_task(consumer(f"worker-{i}", queue))
        tasks.append(task)

    # Nothing more to do but wait until all work is fully processed
    start_ts = time.perf_counter()
    await queue.join()
    real_wait_time = time.perf_counter() - start_ts

    # Because consumers are infinite loops, we need to cancel them
    for task in tasks:
        task.cancel()

    # Wait until all consumers are cancelled, don't fail on exceptions
    await asyncio.gather(*tasks, return_exceptions=True)

    # Final report
    print("=" * 80)
    print(f"{len(tasks)} tasks processed")
    print(f"Processed {total_sleep_time:.3f} seconds in {real_wait_time:.3f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
