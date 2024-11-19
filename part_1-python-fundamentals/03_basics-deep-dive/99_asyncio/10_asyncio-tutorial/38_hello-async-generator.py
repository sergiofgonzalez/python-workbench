"""Illustrate (again) how to create an async generator."""

import asyncio
import time
from collections.abc import AsyncGenerator
from random import randint

from rich import print

colors_by_dice = {}


async def async_rand_int(max_nums: int = 10) -> AsyncGenerator[int, None]:
    """Async generator that returns up to max_num random ints."""
    for _ in range(max_nums):
        yield randint(1, 6)


async def better_async_rand_int(
    max_nums: int = 10,
) -> AsyncGenerator[int, None]:
    """
    Async generator that returns up to max_num random ints implemented in a way
    that allows for cooperating coroutines.
    """
    for _ in range(max_nums):
        await asyncio.sleep(0)
        yield randint(1, 6)


async def throw_dice(
    times: int,
    dice_id: str = "dice #1",
    *,
    use_better: bool = False,
) -> dict[int, int]:
    """Simulate the throw of a dice a number of times, asynchronously."""
    dice_color = 10 + len(colors_by_dice)
    colors_by_dice[dice_id] = dice_color
    print(f"{colors_by_dice}")
    results = {k: 0 for k in range(1, 7)}
    num_results = 0
    if not use_better:
        gen_fn = async_rand_int(times)
    else:
        gen_fn = better_async_rand_int(times)
    async for value in gen_fn:
        results[value] += 1
        num_results += 1
        if num_results % 1000 == 0:
            print(f"[color({dice_color})]{dice_id}: {num_results}")
    return dice_id, results


async def main() -> None:
    """Async entry point."""
    i = 0
    async for num in async_rand_int():
        i += 1
        print(f"{i}: {num}")

    # you can also iterate manually over the async generator iterator
    it = async_rand_int()
    for i in range(5):
        val = await anext(it)
        print(f"{i}: {val}")

    # Note that tasks won't cooperate unless you await in the async generator
    print("=" * 80)
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        task_dice_1 = group.create_task(throw_dice(100_000, "dice #1"))
        task_dice_2 = group.create_task(throw_dice(100_000, "dice #2"))
    print(task_dice_1.result())
    print(task_dice_2.result())
    print(f"Process took {time.perf_counter() - start:.3f} seconds")

    # Better implementation that cooperate
    # Note: it'll take more time, but you'll see how the tasks release
    # the control to each other
    print("=" * 80)
    start = time.perf_counter()
    async with asyncio.TaskGroup() as group:
        task_dice_1 = group.create_task(
            throw_dice(100_000, "dice #3", use_better=True),
        )
        task_dice_2 = group.create_task(
            throw_dice(100_000, "dice #4", use_better=True),
        )
    print(task_dice_1.result())
    print(task_dice_2.result())
    print(f"Process took {time.perf_counter() - start:.3f} seconds")


if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
