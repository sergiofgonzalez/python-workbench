"""Async generator."""

import asyncio
from collections.abc import AsyncGenerator

from rich import print

colors = {
    "g": "green",
    "h": "magenta",
}


async def my_async_generator(
    name: str, u: int = 10,
) -> AsyncGenerator[int, None]:
    """Yield powers of two until the given threshold is exceeded."""
    i = 0
    while i < u:
        print(f">>> [{colors[name]}]{name} working[/{colors[name]}]")
        yield 2**i
        i += 1
        # suspend for 0.1 seconds
        await asyncio.sleep(0.1)


async def main() -> tuple[list[int], list[int]]:
    """Obtain two async list comprehensions and return them."""
    g = [i async for i in my_async_generator("g")]
    h = [j async for j in my_async_generator("h") if not (j // 3 % 5)]
    return g, h


if __name__ == "__main__":
    g, h = asyncio.run(main())
    print(f"{g=}")
    print(f"{h=}")
