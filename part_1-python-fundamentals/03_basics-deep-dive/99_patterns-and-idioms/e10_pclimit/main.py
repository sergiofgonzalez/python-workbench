"""Illustrate the use of the WorkQueue with a p-limit-ish dev experience."""

import asyncio
import time

from pclimit import PCLimit

even_nums = []
odd_nums = []


async def classify_in_even_odd(num: int) -> None:
    """Classify a number into even or odd."""
    if num % 2 == 0:
        even_nums.append(num)
    else:
        odd_nums.append(num)


async def main() -> None:
    """Async application entry point."""
    start = time.perf_counter()
    async with PCLimit(concurrency=2) as pclimit:
        for i in range(1_000_000):
            await pclimit.run(classify_in_even_odd, i)
    print(f"Process took {time.perf_counter() - start:.3f} seconds")  # noqa: T201


if __name__ == "__main__":
    asyncio.run(main())
