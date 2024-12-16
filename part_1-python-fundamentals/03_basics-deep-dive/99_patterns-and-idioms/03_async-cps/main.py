"""Asynchronous Continuation-Passing Style in Python."""

import asyncio


def when_done_cb(task: asyncio.Task) -> None:
    """Execute logic when async task has completed."""
    print(f">>> task completed: {task.done()=}, {task.cancelled()=}")
    if not task.cancelled():
        print(f"Task completed: {task.result()}")
    else:
        print("For some reason the task was cancelled.")


async def add(a: float, b: float) -> float:
    """Async add using CPS style."""
    print(f">>> executing add({a=}, {b=})")
    await asyncio.sleep(0.1)
    return a + b


async def main() -> None:
    """Application entry point."""
    add_task = asyncio.create_task(add(2, 3))
    add_task.add_done_callback(when_done_cb)
    # If you comment the following block, the task will be cancelled
    if not add_task.done():
        print(">>> awaiting for add_task() to complete")
        await add_task


if __name__ == "__main__":
    asyncio.run(main())
