"""Illustrates asyncio.gather."""

import asyncio
import time


async def reverse_async(seq: list[int]) -> list[int]:
    """Resemble an I/O bound task that reverses a list."""
    await asyncio.sleep(max(seq))
    return list(reversed(seq))


async def main() -> None:
    """Run a couple of tasks in parallel using asyncio.gather."""
    start = time.perf_counter()
    coro1 = reverse_async([1, 2, 3])
    coro2 = reverse_async([3, 2, 1])
    l1, l2 = await asyncio.gather(coro1, coro2)
    print(f"Completed: took {time.perf_counter() - start:0.3f} seconds.")
    print(f"{l1=}")
    print(f"{l2=}")


if __name__ == "__main__":
    asyncio.run(main())
