"""Illustrates asyncio.TaskGroup usage (introduced in Python 3.11)."""

import asyncio
import random


async def coro(delay: int, *, should_fail: bool = False) -> int:
    """Sleep for `delay` seconds and returns it."""
    await asyncio.sleep(delay)
    if should_fail:
        msg = f"coro failed after {delay} seconds"
        raise RuntimeError(msg)
    return delay


async def main() -> None:
    """Async application entry point."""
    # Scenario 1: single task in the group, results available without awaiting
    # (after the context manager exits)
    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(coro(delay=2), name="task-2s")

    print(
        f"Tasks in TaskGroup have completed: slept for {task.result()} seconds",
    )
    print("=" * 40)

    # Scenario 2: using await on one of the tasks in the group while the group
    # is active
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(coro(delay=3), name="task-3s")
        task2 = tg.create_task(coro(delay=5), name="task-5s")

        # explicitly await task1
        result1 = await task1
        print(f"task1 completed first: slept for {result1} seconds")

    result2 = task2.result()
    print(f"task2 completed upon exit: slept for {result2} seconds")
    print("=" * 40)

    # Scenario 3: simulating asyncio.gather() behavior with multiple tasks
    # that don't fail
    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(
                coro(delay=i),
                name=f"task-{i}s",
            )
            for i in range(5)
        ]
    for task in tasks:
        try:
            result = task.result()
            print(f"{task.get_name()}: completed successfully with result {result}")
        except Exception as e:  # noqa: BLE001
            print(f"{task.get_name()}: raised an exception: {e}")
    print("=" * 40)

    # Scenario 4: simulating asyncio.gather() behavior with multiple tasks
    # that may fail
    try:
        async with asyncio.TaskGroup() as tg:
            tasks = [
                tg.create_task(
                    coro(delay=i, should_fail=random.choice([True, False])),  # noqa: S311
                    name=f"task-{i}s",
                )
                for i in range(5)
            ]
    except* RuntimeError as e:
        print(f"Caught exceptions from tasks: {e.exceptions}")
        for task in tasks:
            if not task.cancelled():
                print(
                    f"{task.get_name()}: done={task.done()}; cancelled={task.cancelled()}; exception={task.exception()}"  # noqa: COM812, E501
                )
            else:
                print(f"{task.get_name()}: done={task.done()}; cancelled={task.cancelled()};")  # noqa: E501
    else:
        for task in tasks:
            try:
                result = task.result()
                print(f"{task.get_name()}: completed successfully with result {result}")
            except Exception as e:  # noqa: BLE001
                print(f"{task.get_name()}: raised an exception: {e}")
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
