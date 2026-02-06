"""Illustrates asyncio task callbacks."""

import asyncio

from rich import print  # noqa: A004


async def do_async(delay: int, *, should_raise: bool = False) -> str:
    """Asynchronously sleep for delay seconds, optionally raising an exception."""
    await asyncio.sleep(delay)
    if should_raise:
        msg = f"An error occurred after {delay} seconds"
        raise RuntimeError(msg)
    return f"Completed after {delay} seconds"


def print_hello_when_done(task: asyncio.Task) -> None:
    """Print a message when the task is done."""
    print(f"[yellow]Task {task.get_name()} is done: {task}[/yellow]")


def print_task_info(task: asyncio.Task) -> None:
    """Print task result or exception."""
    if task.cancelled():
        print(f"[green]Task {task.get_name()} was cancelled.[/green]")
    elif task.exception() is not None:
        print(
            f"[green]Task {task.get_name()} raised an exception: {task.exception()}[/green]",  # noqa: E501
        )
    else:
        print(
            f"[green]Task {task.get_name()} completed with result: {task.result()}[/green]",  # noqa: E501
        )


async def main() -> None:
    """Async application entry point."""
    task = asyncio.create_task(do_async(2, should_raise=False), name="do-async-ok")
    task.add_done_callback(print_hello_when_done)
    task.add_done_callback(print_task_info)
    try:
        await task
    except Exception as e:  # noqa: BLE001
        print(f"[cyan]Caught exception awaiting task: {e}[/cyan]")
    print("=" * 40)

    task = asyncio.create_task(do_async(2, should_raise=True), name="do-async-error")
    task.add_done_callback(print_hello_when_done)
    task.add_done_callback(print_task_info)
    try:
        await task
    except Exception as e:  # noqa: BLE001
        print(f"[cyan]Caught exception awaiting task: {e}[/cyan]")


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
