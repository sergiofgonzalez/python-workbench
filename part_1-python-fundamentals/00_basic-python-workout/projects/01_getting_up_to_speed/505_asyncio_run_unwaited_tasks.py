"""Illustrates that a program can finish before all tasks are complete."""

import asyncio


async def reverse_async(nums: list[int]) -> list[int]:
    """Reverse a list of integers asynchronously."""
    await asyncio.sleep(max(nums))  # Simulate some async work
    result = list(reversed(nums))
    print("Reversed completed: result is", result)
    return result


async def main() -> None:
    """Async application entry point."""
    asyncio.create_task(reverse_async([1, 2, 3]))  # noqa: RUF006


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
    # The program may exit before the unwaited task is complete.
    # you won't see "Reversed completed: ..." printed.
