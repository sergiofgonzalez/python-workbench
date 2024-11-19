"""Illustrates asyncio.gather to run iterators in parallel."""

import asyncio
import time
from collections.abc import AsyncGenerator

from rich import print

colors = {
    "g": "green",
    "h": "magenta",
}


async def my_async_generator(
    name: str,
    u: int = 10,
) -> AsyncGenerator[int, None]:
    """Yield powers of two until certain number of samples is reached."""
    i = 0
    while i < u:
        print(f">>> [{colors[name]}]{name} working[/{colors[name]}]")
        yield 2**i
        i += 1
        # suspend for 0.1 seconds
        await asyncio.sleep(0.1)


async def wrap_gen(name: str) -> list[int]:
    """Wrap an async generator so that it can be run in parallel."""
    return [i async for i in my_async_generator(name)]


async def main() -> None:
    """Run a couple of tasks in parallel using asyncio.gather."""
    start = time.perf_counter()
    t1 = asyncio.create_task(wrap_gen("g"))
    t2 = asyncio.create_task(wrap_gen("h"))
    l1, l2 = await asyncio.gather(t1, t2)
    print(f"Completed: took {time.perf_counter() - start:0.3f} seconds.")
    print(f"{l1=}")
    print(f"{l2=}")


if __name__ == "__main__":
    asyncio.run(main())
