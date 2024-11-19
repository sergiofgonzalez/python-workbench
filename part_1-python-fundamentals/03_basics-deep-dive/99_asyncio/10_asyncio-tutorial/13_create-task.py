"""Illustrate the use of create_task to schedule the execution of coroutines."""

import asyncio


async def reverse_async(seq: list[int]) -> list[int]:
    """Resemble an I/O bound task that reverses a list."""
    await asyncio.sleep(max(seq))
    return list(reversed(seq))


async def main() -> None:
    """Schedules the execution of the coroutine using create_task."""
    t = asyncio.create_task(reverse_async([1, 2, 3]))
    await t
    print(f"t: type {type(t)}")
    print(f"t done: {t.done()}")


if __name__ == "__main__":
    asyncio.run(main())
