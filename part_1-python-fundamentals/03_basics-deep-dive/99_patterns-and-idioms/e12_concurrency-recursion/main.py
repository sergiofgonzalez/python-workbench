"""Illustrate caveats that might pop up when you mix recursion and limited concurrency."""

import asyncio

from pclimit import PCLimit


async def factorial(num: int) -> int:
    """Compute factorial asynchronously."""
    if num == 1:
        return 1
    tmp = await factorial(num - 1)
    return num * tmp


async def pc_factorial(num: int, pclimit: PCLimit) -> int:
    """Calculate the factorial with limited parallel concurrency."""
    if num == 1:
        return 1
    future = await pclimit.run(pc_factorial, num - 1, pclimit)
    if not future.done():
        await future
    return num * future.result()


async def main() -> None:
    """Async application entry point."""
    # running this with unlimited parallel concurrency is OK
    result = await factorial(5)
    print(f"5! = {result}")

    # but with limited pc is tricky
    print("=" * 80)
    async with PCLimit(concurrency=10) as pclimit:
        result = await pc_factorial(5, pclimit)
    print(result)

    # if we bring down the number of workers, the process stalls in a deadlock
    print("=" * 80)
    async with PCLimit(concurrency=3) as pclimit:
        result = await pc_factorial(5, pclimit)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
