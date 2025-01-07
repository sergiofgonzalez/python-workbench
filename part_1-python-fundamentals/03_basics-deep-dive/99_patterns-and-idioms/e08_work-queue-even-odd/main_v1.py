"""Using WorkQueue to classify a large list of numbers into even and odd."""

import asyncio
import time

even_nums = []
odd_nums = []


def is_even(num: int) -> bool:
    """Return True if num is even, False otherwise."""
    return num % 2 == 0


async def consumer(name: str, work_queue: asyncio.Queue) -> None:
    """Worker part of the solution."""
    started_working = False
    print(f">>> {name} ready to work")
    while True:
        num = await work_queue.get()
        if not started_working:
            started_working = True
            print(f">>> {name} has started consuming")
            was_even = await asyncio.to_thread(is_even, num)
            if was_even:
                even_nums.append(num)
            else:
                odd_nums.append(num)
        work_queue.task_done()


async def classify_even_odd_numbers(
    num_count: int,
    concurrency: int = 2,
) -> tuple[list[int], list[int]]:
    """Classify a large list of numbers into even and odd asynchronously."""
    # Create the work queue
    work_queue = asyncio.Queue()

    # Spin up the workers, keeping track of the tasks they run im
    tasks = []
    for i in range(concurrency):
        task = asyncio.create_task(consumer(f"worker-{i}", work_queue))
        tasks.append(task)

    # Start pushing work items in the work queue
    for i in range(num_count):
        await work_queue.put(i)
        if i % 100 == 0:
            print(f">>> {i} numbers produced")

    # Wait until everything done
    print(">>> Production complete")
    await work_queue.join()
    print(">>> Consumption complete")

    # Cancell the workers
    for task in tasks:
        task.cancel()
    asyncio.gather(*tasks, return_exceptions=True)


async def main() -> None:
    """Async application entry point."""
    start = time.perf_counter()
    await classify_even_odd_numbers(1_000_000, concurrency=10)
    print(f"Process took {time.perf_counter() - start:.6f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
