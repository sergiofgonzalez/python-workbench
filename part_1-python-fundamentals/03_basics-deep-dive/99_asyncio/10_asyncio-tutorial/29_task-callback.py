"""Illustrate how to register and deregister a done callback for a task."""

import asyncio

from rich import print


def print_hello_when_done(task: asyncio.Task) -> None:
    """Print hello when the task is done."""
    print(f"[blue]hello, world!: Task {task.get_name()} was done[/blue]")
    print(f"[blue]{task=}[/blue]")


def print_some_task_info(task: asyncio.Task) -> None:
    """Print info about the task when the task is done."""
    print(f"[yellow]Info about task {task.get_name()}[/yellow]")
    if task.cancelled():
        print("[yellow]The task was cancelled[/yellow]")
    if not task.exception():
        print(
            "[yellow]The task ended successfully:[/yellow]"
            f"result = {task.result()}",
        )
    else:
        exception = task.exception()
        print(f"[yellow]The task failed with: {exception}[/yellow]")


async def do_async(delay_sec: int, *, should_raise: bool) -> str:
    """Wait for the given seconds and return."""
    await asyncio.sleep(delay_sec)
    if should_raise:
        msg = "I was told to raise."
        raise RuntimeError(msg)
    return "finished successfully"


async def main() -> None:
    """App entry point."""
    task = asyncio.create_task(
        do_async(2, should_raise=False),
        name="Success after 2 secs task.",
    )
    task.add_done_callback(print_hello_when_done)
    task.add_done_callback(print_some_task_info)
    if not task.done():
        await task

    # Now with a failed task
    print("=" * 80)
    task = asyncio.create_task(
        do_async(5, should_raise=True),
        name="Failure after 5 secs task.",
    )
    task.add_done_callback(print_hello_when_done)
    task.add_done_callback(print_some_task_info)
    if not task.done():
        task.remove_done_callback(print_hello_when_done)
        try:
            await task
        except Exception as e:  # noqa: BLE001
            print(f"Yeah, I told the task to fail: {e}")


if __name__ == "__main__":
    # Start an  event loop in the current thread and send main() to execution
    asyncio.run(main())
