"""Illustrates how to use asyncio.as_completed."""

import asyncio


async def reverse_async(nums: list[int]) -> tuple[list[int], str]:
    """Reverse a list of integers asynchronously."""
    await asyncio.sleep(max(nums))  # Simulate some async work
    result = list(reversed(nums))
    print("Reversed completed: result is", result)
    task_name = asyncio.current_task().get_name()  # type: ignore[union-attr]
    return result, task_name


async def main() -> None:
    """Async application entry point."""
    tasks = [
        asyncio.create_task(reverse_async([4, 5, 6]), name="task-med"),
        asyncio.create_task(reverse_async([7, 8, 9]), name="task-long"),
        asyncio.create_task(reverse_async([1, 2, 3]), name="task-short"),
    ]
    for completed_task in asyncio.as_completed(tasks):
        result, task_name = await completed_task
        print(f"Got result for task {task_name}:", result)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
