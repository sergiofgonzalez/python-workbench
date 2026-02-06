"""Illustrates the basics of asyncio queues to coordinate workers and consumers."""

import asyncio
import random
import time

import rich


async def worker(worker_id: int, queue: asyncio.Queue[float]) -> None:
    """Worker that processes items from a queue."""
    color = f"color({worker_id})"
    while True:
        item = await queue.get()
        rich.print(f"[{color}]Worker {worker_id}: processing item: {item}[/{color}]")
        await asyncio.sleep(item)  # Simulate work
        queue.task_done()
        rich.print(f"[{color}]Worker {worker_id}: finished item: {item}[/{color}]")


async def main() -> None:
    """Async application entry point."""
    queue: asyncio.Queue[float] = asyncio.Queue()
    total_delay = 0.0
    for _ in range(20):
        item = random.uniform(0.05, 1.0)  # noqa: S311
        await queue.put(item)
        rich.print(f"Added item to queue: {item}")
        total_delay += item

    # Start worker tasks
    start_time = time.perf_counter()
    workers = [asyncio.create_task(worker(idx, queue)) for idx in range(3)]

    await queue.join()  # Wait until all items are processed
    end_time = time.perf_counter()
    rich.print(f"Total elapsed time: {end_time - start_time:.2f} seconds")
    rich.print(f"Total sleep  time: {total_delay:.2f} seconds")

    for w in workers:
        w.cancel()  # Cancel worker tasks

    # Wait until all worker tasks are cancelled, supressing exceptions
    await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
