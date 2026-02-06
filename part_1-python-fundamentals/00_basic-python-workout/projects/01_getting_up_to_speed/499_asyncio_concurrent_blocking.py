"""Illustrates how to run concurrent blocking code."""

import asyncio
import re
import time

import rich


async def count_to_10(name: str, *, yield_control: bool = False) -> None:
    """Count to 10 with no delays, thus preventing cooperation."""
    match = re.match(r"Task-(\d+)", name)
    task_num = int(match.group(1)) if match else 0

    for i in range(10):
        rich.print(
            f"[bold color({task_num})]{name}[/bold color({task_num})] counting: "
            f"{i + 1}",
        )
        if yield_control:
            await asyncio.sleep(0)


async def main() -> None:
    """Async application entry point."""
    # Scenario 1: multiple blocking tasks prevent cooperation
    start_ts = time.perf_counter()
    tasks = [asyncio.create_task(count_to_10(f"Task-{i + 1}")) for i in range(5)]
    await asyncio.gather(*tasks)
    print(f"Total time taken: {time.perf_counter() - start_ts:.6f} seconds")
    print("=" * 40)

    # Scenario 2: using asyncio.sleep(0) to yield control and allow cooperation
    start_ts = time.perf_counter()
    tasks = [
        asyncio.create_task(count_to_10(f"Task-{i + 1}", yield_control=True))
        for i in range(5)
    ]
    await asyncio.gather(*tasks)
    print(f"Total time taken: {time.perf_counter() - start_ts:.6f} seconds")
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
