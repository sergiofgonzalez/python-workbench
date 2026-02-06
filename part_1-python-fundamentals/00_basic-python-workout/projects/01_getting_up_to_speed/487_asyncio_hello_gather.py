"""Illustrates asyncio.gather usage with a basic example."""

import asyncio
import random

import rich


async def rand_sleep_async(max_sleep: int, task_index: int) -> int:
    """Asynchronously sleep for a random duration up to max_sleep seconds."""
    sleep_time = random.randint(0, max_sleep)  # noqa: S311
    rich.print(
        f"[color({task_index})]"
        f"Sleeping for {sleep_time:.2f} seconds...[/color({task_index})]",
    )
    await asyncio.sleep(sleep_time)
    rich.print(
        f"[color({task_index})]"
        f"Slept for {sleep_time:.2f} seconds.[/color({task_index})]",
    )
    return int(sleep_time)


async def main(*sleep_values: int) -> None:
    """Async application entry point."""
    # Lab1: awaiting syncio.gather()
    results = await asyncio.gather(
        *(
            rand_sleep_async(sleep_val, index)
            for index, sleep_val in enumerate(sleep_values)
        ),
    )
    rich.print(f"[bold]All tasks completed. Results: {results}[/bold]")
    rich.print("-" * 40)

    # Lab2: getting the Future from asyncio.gather() and awaiting it later
    gather_future = asyncio.gather(
        *(
            rand_sleep_async(sleep_val, index)
            for index, sleep_val in enumerate(sleep_values)
        ),
    )
    rich.print("[bold]Doing other work while tasks run...[/bold]")
    await asyncio.sleep(0.5)
    if not gather_future.done():
        rich.print("[bold]Tasks are still running...[/bold]")
    await gather_future
    rich.print("[bold]All tasks completed.")
    if gather_future.done():
        try:
            results = gather_future.result()
            rich.print(f"[bold]Results: {results}[/bold]")
        except Exception as exc:  # noqa: BLE001
            rich.print(f"[bold]An error occurred: {exc}[/bold]")
            rich.print(gather_future.exception())


if __name__ == "__main__":
    # start the event loop in the current thread and schedule main() to run.
    asyncio.run(main(3, 5, 2, 4, 1))
