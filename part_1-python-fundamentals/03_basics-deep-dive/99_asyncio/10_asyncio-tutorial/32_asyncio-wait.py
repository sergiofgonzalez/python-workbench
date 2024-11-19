"""Illustrates how to use asyncio.wait()."""

import asyncio
import time
from random import randint

from rich import print


async def my_coroutine(*, may_raise: bool = False) -> int:
    """Sleep async for a random number of seconds and return the value."""
    value = randint(0, 5)
    await asyncio.sleep(value)
    if may_raise and randint(0, 10) > 8:  # noqa: PLR2004
        current_task = asyncio.current_task()
        print(
            f"[yellow]Task {current_task.get_name()!r} will raise[/yellow]"  # noqa: COM812
        )
        msg = "This will raise!"
        raise RuntimeError(msg)

    current_task = asyncio.current_task()
    print(
        f"[yellow]Task {current_task.get_name()!r} done with value {value}[/yellow]"  # noqa: COM812, E501
    )
    return value


async def main() -> None:
    """Async app entry point."""
    # wait for all tasks completed, no timeout
    tasks = [
        asyncio.create_task(my_coroutine(), name=f"t_{i}") for i in range(5)
    ]
    start = time.perf_counter()
    done, pending = await asyncio.wait(tasks)
    if len(done) == len(tasks):
        print("\nAll tasks were completed:")
        for task in done:
            print(f"{task.get_name()}: {task.result()}")
    else:
        print("\nNot all tasks were completed")

    print(
        f"[white]process took: {time.perf_counter() - start:.3f} second(s).[/white]",  # noqa: E501
    )
    print("=" * 80, end="\n\n")

    # wait for all tasks to be completed, with a timeout
    tasks = [
        asyncio.create_task(my_coroutine(), name=f"t_{i}") for i in range(5)
    ]
    start = time.perf_counter()
    done, pending = await asyncio.wait(tasks, timeout=3)
    if len(done) == len(tasks):
        print("\nAll tasks were completed:")
        for task in done:
            print(f"{task.get_name()}: {task.result()}")
    else:
        print("\nNot all tasks were completed")
        print("Done:")
        for task in done:
            print(f"\t{task.get_name()}: {task.result()}")
        print("Pending:")
        for task in pending:
            print(f"\t{task.get_name()}: N/A")

    print(
        f"[white]process took: {time.perf_counter() - start:.3f} second(s).[/white]",  # noqa: E501
    )
    print("=" * 80, end="\n\n")

    # wait for first task to be completed, with a timeout
    tasks = [
        asyncio.create_task(my_coroutine(), name=f"t_{i}") for i in range(5)
    ]
    start = time.perf_counter()
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_COMPLETED,
        timeout=3,
    )
    if len(done) == len(tasks):
        print("\nAll tasks were completed:")
        for task in done:
            print(f"{task.get_name()}: {task.result()}")
    else:
        print("\nNot all tasks were completed")
        print("Done:")
        for task in done:
            print(f"\t{task.get_name()}: {task.result()}")
        print("Pending:")
        for task in pending:
            print(f"\t{task.get_name()}: N/A")

    print(
        f"[white]process took: {time.perf_counter() - start:.3f} second(s).[/white]",  # noqa: E501
    )
    print("=" * 80, end="\n\n")

    # wait for first task to raise
    tasks = [
        asyncio.create_task(my_coroutine(may_raise=True), name=f"t_{i}")
        for i in range(5)
    ]
    start = time.perf_counter()
    done, pending = await asyncio.wait(
        tasks,
        return_when=asyncio.FIRST_EXCEPTION,
    )
    if len(done) == len(tasks):
        print("\nAll tasks were completed before first exception:")
        for task in done:
            if not task.exception():
                print(f"\t{task.get_name()}: {task.result()}")
            else:
                print(f"\t{task.get_name()}: (raised)")
    else:
        print("\nNot all tasks were completed before first exception")
        print("Done:")
        for task in done:
            if not task.exception():
                print(f"\t{task.get_name()}: {task.result()}")
            else:
                print(f"\t{task.get_name()}: (raised)")
        print("Pending:")
        for task in pending:
            print(f"\t{task.get_name()}: N/A")

    print(
        f"[white]process took: {time.perf_counter() - start:.3f} second(s).[/white]"  # noqa: COM812, E501
    )
    print("=" * 80, end="\n\n")


if __name__ == "__main__":
    asyncio.run(main())
