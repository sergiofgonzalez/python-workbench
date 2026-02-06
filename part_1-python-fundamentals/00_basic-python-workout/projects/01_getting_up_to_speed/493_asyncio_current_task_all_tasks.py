"""Illustrate asyncio current_task and all_tasks."""

import asyncio
import re
from datetime import UTC, datetime

from rich import print  # noqa: A004


async def long_running_task(delay_sec: int) -> None:
    """Simulate a long-running synchronous task."""
    match = re.match(
        r"long-runner-(?P<task_id>\d+)s",
        asyncio.current_task().get_name(),  # ty:ignore[possibly-missing-attribute]
    )
    color_id = match.group("task_id") if match else 0

    while True:
        print(
            f"[color({color_id})]{datetime.now(UTC)}: long_running_task(): "
            f"sleeping for {delay_sec} seconds[/color({color_id})]",
        )
        await asyncio.sleep(delay_sec)


async def main() -> None:
    """Async application entry point."""
    asyncio.create_task(long_running_task(3), name="long-runner-3s")  # noqa: RUF006
    asyncio.create_task(long_running_task(5), name="long-runner-5s")  # noqa: RUF006

    while True:
        await asyncio.sleep(1)
        current_task = asyncio.current_task()
        all_tasks = asyncio.all_tasks()
        print(
            f"[green]{datetime.now(UTC)}: "
            f"Current task: {current_task.get_name() if current_task else None}: "
            f" ({current_task.get_coro().__name__})[/green]",  # ty:ignore[possibly-missing-attribute]
        )
        print(f"[green]{datetime.now(UTC)}: All tasks:[/green]")
        for t in all_tasks:
            print(f"    [green]- {t.get_name()}[/green]")
        print("-" * 60)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[red]Received keyboard interrupt, exiting...[/red]")
