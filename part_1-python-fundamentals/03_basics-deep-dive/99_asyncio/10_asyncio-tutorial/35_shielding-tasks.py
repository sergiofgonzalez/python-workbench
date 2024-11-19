"""Illustrate how to use shield() to prevent tasks from being cancelled."""

import asyncio


async def my_coroutine(num: int) -> int:
    """Return the passed integer argument after async sleeping for one sec."""
    await asyncio.sleep(1)
    return num


async def cancel_task(t: asyncio.Task) -> None:
    """Cancel the given task after async sleeping for a fraction of a second."""
    await asyncio.sleep(0.2)
    t.cancel()


def print_task_status(label: str, t: asyncio.Task) -> None:
    """Print the task status."""
    print(
        f"Task {label}: done={t.done()}, cancelled={t.cancelled()}, result={t.result() if t.done() and not t.cancelled() and not t.exception() else 'n/a'}, exception={t.exception() if t.done() and not t.cancelled() and t.exception() else 'None'}",  # noqa: E501
    )


async def main() -> None:
    """Async coroutine that serves as entry point."""
    # Run the task in isolation
    task = asyncio.create_task(my_coroutine(1))
    if not task.done():
        await task
    print_task_status("task", task)

    # Run the task cancelling it (raises an exception)
    print("=" * 80)
    task = asyncio.create_task(my_coroutine(1))
    cancelling_task = asyncio.create_task(cancel_task(task))
    if not cancelling_task.done():
        await cancelling_task
    print_task_status("task", task)
    print_task_status("cancelling_task", cancelling_task)

    # Run the task shielding it
    # You should see that the task returns, even when the cancelling task
    # finished
    print("=" * 80)
    task = asyncio.create_task(my_coroutine(1))
    shielded_task = asyncio.shield(task)
    cancelling_task = asyncio.create_task(cancel_task(shielded_task))
    if not task.done():
        await task
    print_task_status("task", task)
    print_task_status("shielded_task", shielded_task)
    print_task_status("cancelling_task", cancelling_task)



if __name__ == "__main__":
    # Start the event loop in the current thread
    asyncio.run(main())
