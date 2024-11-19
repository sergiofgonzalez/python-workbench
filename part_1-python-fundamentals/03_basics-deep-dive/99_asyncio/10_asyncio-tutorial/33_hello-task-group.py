"""Illustrate the basic behavior of the TaskGroup context manager."""

import asyncio
import time

from rich import print


async def my_coroutine(*, delay: int = 1, should_fail: bool = False) -> str:
    """
    Wait asynchronously for the specified delay, then return a string,
    optionally failing.
    """
    print(
        f"[yellow]Will wait for {delay} sec and will {'not fail.' if not should_fail else 'fail.' }[/yellow]"
    )  # noqa: E501
    await asyncio.sleep(delay)
    if should_fail:
        raise RuntimeError("I was told to fail")  # noqa: EM101, TRY003
    msg = f"I waited for {delay} seconds"
    print(f"[yellow]{msg}[/yellow]")
    return f"I waited for {delay} seconds"


async def main() -> None:
    """Async app entry point."""
    # # single task: auto await upon exit
    # async with asyncio.TaskGroup() as group:
    #     group.create_task(my_coroutine(delay=3))
    # print("Here the task has been automatically awaited")

    # multiple tasks: explicitly awaiting some tasks
    # print("=" * 80)
    # start = time.perf_counter()
    # async with asyncio.TaskGroup() as group:
    #     task = group.create_task(my_coroutine(delay=3))
    #     group.create_task(my_coroutine(delay=5))
    #     if not task.done():
    #         result = await task
    #         print(f"Task completed: {result} (took {time.perf_counter() - start:.3f} seconds)")  # noqa: E501
    # print(f"All the tasks in the TaskGroup has been done by now (took {time.perf_counter() - start:.3f} seconds)")  # noqa: E501

    # managing results of multiple tasks à la asyncio.gather
    # within the context manager, you're free to use any of the asyncio
    # idioms, which gives you a lot of freedom
    # print("=" * 80)
    # async with asyncio.TaskGroup() as group:
    #     tasks = [group.create_task(my_coroutine(delay=i)) for i in range(5)]
    # print(
    #     "All the tasks in the TaskGroup has been done by now (no exception raised)"  # noqa: COM812, E501
    # )
    # results = [task.result() for task in tasks]
    # print(results)

    # multiple tasks: the first one fails, the second should be cancelled and
    # therefore I shouldn't be seeing any side effects from the second
    # Note that the proper way to deal with exceptions within the group is to
    # wrap the context manager within a try-block.
    # Individual exceptions can also be handled within the context manager block
    print("=" * 80)
    start = time.perf_counter()
    try:
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(my_coroutine(delay=3)),
                group.create_task(my_coroutine(delay=5, should_fail=True)),
                group.create_task(my_coroutine(delay=7)),
            ]
        print(
            f"All the tasks in the TaskGroup has been done by now (took {time.perf_counter() - start:.3f} seconds)"
        )  # noqa: E501
    except Exception as e:
        print(f"Something failed while processing the TaskGroup: {type(e)} {e}")

    for i, task in enumerate(tasks):
        print(f"[white]Task #{i}: done={task.done()}, cancelled={task.cancelled()}, result={task.result() if not task.cancelled() and not task.exception() else 'N/A'}, exception={task.exception() if not task.cancelled() and task.exception() else "N/A"}[/white]")  # noqa: E501

if __name__ == "__main__":
    # Start the event loop in the curren thread
    asyncio.run(main())
