"""Illustrate the use of create_task to schedule the execution of coroutines."""

import asyncio


async def reverse_async(seq: list[int]) -> list[int]:
    """Resemble an I/O bound task that reverses a list."""
    await asyncio.sleep(max(seq))
    return list(reversed(seq))


async def delayed_print(msg: str, num_seconds: int) -> None:
    """Print a message after the given number of seconds."""
    await asyncio.sleep(num_seconds)
    print(msg)


async def main() -> None:
    """Schedules the execution of the coroutine using create_task."""
    t1 = asyncio.create_task(reverse_async([1, 2, 3]))
    t2 = asyncio.create_task(delayed_print("hello, asyncio!", 5))
    await t1
    print(f"t1: type {type(t1)}")
    print(f"t done: {t1.done()}")


if __name__ == "__main__":
    asyncio.run(main())
