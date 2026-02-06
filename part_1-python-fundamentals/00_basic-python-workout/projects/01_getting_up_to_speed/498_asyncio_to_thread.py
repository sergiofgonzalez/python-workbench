"""Illustrate asyncio.to_thread() to run blocking tasks on a separate thread."""

import asyncio
import time

import rich


async def long_running_task(
    num_steps: int = 5,
    step_delay: float = 0.5,
    color_idx: int = 1,
) -> None:
    """Simulate a long-running well-behaved (cooperative) task."""
    task_name = asyncio.current_task().get_name()  # ty:ignore[possibly-missing-attribute]
    progress_bar = "[" + " " * num_steps + "] (0%)"
    rich.print(f"[color({color_idx})]{task_name}: {progress_bar}[/color({color_idx})]")
    for step in range(num_steps):
        await asyncio.sleep(step_delay)  # Simulate blocking operation
        pct = int(((step + 1) / num_steps) * 100)
        rich.print(
            f"[color({color_idx})]{task_name}: ["
            + "=" * (step + 1)
            + " " * (num_steps - step - 1)
            + f"] ({pct} %)[/color({color_idx})]",
        )
    rich.print(
        f"[color({color_idx})]{task_name}: Long-running task completed.[/color({color_idx})]",  # noqa: E501
    )


def sync_blocking_call(
    num_steps: int = 5,
    step_delay: float = 0.5,
    color_idx: int = 1,
    label: str = "",
) -> None:
    """Simulate a long-running blocking call that doesn't cooperate with other coros."""
    progress_bar = "[" + " " * num_steps + "] (0%)"
    rich.print(
        f"[color({color_idx})]{label}: Starting blocking long-running task:\n{progress_bar}[/color({color_idx})]",  # noqa: E501
    )
    for step in range(num_steps):
        time.sleep(step_delay)  # Simulate blocking operation
        pct = int(((step + 1) / num_steps) * 100)
        rich.print(
            f"[color({color_idx})]{label}: ["
            + "~" * (step + 1)
            + " " * (num_steps - step - 1)
            + f"] ({pct} %)[/color({color_idx})]",
        )
    rich.print(
        f"[color({color_idx})]{label}: Blocking task completed.[/color({color_idx})]",
    )


async def wrap_sync_blocking_call(
    num_steps: int = 5,
    step_delay: float = 0.5,
    color_idx: int = 1,
) -> None:
    """Async wrapper to run sync blocking call in asyncion programs."""
    return sync_blocking_call(
        num_steps=num_steps,
        step_delay=step_delay,
        color_idx=color_idx,
        label=asyncio.current_task().get_name(),  # ty:ignore[possibly-missing-attribute]
    )


async def main() -> None:
    """Async application entry point."""
    # well-behaved long-running task by itself
    task = asyncio.create_task(long_running_task())
    await task
    print("=" * 40)

    # blocking call by itself
    sync_blocking_call()
    print("=" * 40)

    # Scenario 1: well-behaved tasks cooperate with each other
    tasks = [asyncio.create_task(long_running_task(color_idx=i + 1)) for i in range(5)]
    await asyncio.gather(*tasks)
    print("=" * 40)

    # Scenario 2: as soon as you put a blocking call in the mix, tasks don't cooperate
    tasks = [asyncio.create_task(long_running_task(color_idx=i + 1)) for i in range(5)]
    tasks.append(asyncio.create_task(wrap_sync_blocking_call(color_idx=6)))
    await asyncio.gather(*tasks)
    print("=" * 40)

    # Scenario 3: as soon as you put a blocking call in the mix, tasks don't cooperate
    tasks = [asyncio.create_task(long_running_task(color_idx=i + 1)) for i in range(5)]
    tasks.append(asyncio.create_task(wrap_sync_blocking_call(color_idx=6)))
    await asyncio.gather(*tasks)
    print("=" * 40)

    # Scenario 4: if you send the blocking call to a separate thread, cooperation
    #  is restored
    tasks = [asyncio.create_task(long_running_task(color_idx=i + 1)) for i in range(5)]
    await asyncio.to_thread(sync_blocking_call, color_idx=6, label="Thread")
    await asyncio.gather(*tasks)
    print("=" * 40)

    # Scenario 5: you don't need to run to_thread() separately
    tasks = [asyncio.create_task(long_running_task(color_idx=i + 1)) for i in range(5)]
    await asyncio.gather(
        *tasks,
        asyncio.to_thread(sync_blocking_call, color_idx=6, label="Thread"),
    )
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
