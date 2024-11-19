"""Illustrate how to work with async comprehensions."""

import asyncio
import time
from collections.abc import AsyncGenerator
from random import randint


async def throw_dice() -> int:
    """Simulate the throwing of a six-sides dice using an async generator."""
    value = randint(1, 6)
    await asyncio.sleep(0)
    return value


async def async_dice_experiment(num_throws: int) -> AsyncGenerator[int, None]:
    """Async iterator for dice throwing experiments."""
    for _ in range(num_throws):
        value = await throw_dice()
        await asyncio.sleep(0)
        yield value


async def main() -> None:
    """Async main coroutine."""
    # async comprehensions
    results = [result async for result in async_dice_experiment(10)]
    print(results)

    # await comprehensions
    start = time.perf_counter()
    awaitables = [throw_dice() for _ in range(10)]
    results = [await result for result in awaitables]
    print(f"Process took {time.perf_counter() - start:.6f} seconds")
    print(results)

    # that renders the same result as asyncio.gather
    start = time.perf_counter()
    awaitables = [throw_dice() for _ in range(10)]
    results = await asyncio.gather(*awaitables)
    print(f"Process took {time.perf_counter() - start:.6f} seconds")
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
