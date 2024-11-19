"""Illustrate the scheduling of coroutines without create_task."""

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
    """Schedules the execution of the coroutine directly."""
    task1 = reverse_async([1, 2, 3])
    task2 = delayed_print("hello, asyncio!", 5)
    await task1
    await task2
    print(f"t1: type {type(task1)}")
    # coroutines do not have a `done` method
    # print(f"t done: {task2.done()}")


if __name__ == "__main__":
    asyncio.run(main())
