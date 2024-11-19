"""Illustrate the difference in behavior between a Task and a coroutine."""

import asyncio

import aiofiles


async def coroutine_with_side_effects(filename: str) -> None:
    """Create a file as a side effect of this coroutine."""
    async with aiofiles.open(filename, "w") as f:
        await f.write("Hello, async world!")
    return f"File {filename} was written"


def done_callback(task: asyncio.Task) -> None:
    """Illustrate a task callback behavior."""
    print(f"{task.done()=}")
    print(f"{task.result()}")


async def main() -> None:
    """
    Illustrate the different behavior of running the coroutine directly or
    wrapped in a Task.
    """
    # A:
    # If you invoke a coroutine directly it doesn't execute
    # (i.e., No file created)
    # coroutine_with_side_effects("z_invoking_the_coroutine.txt")

    # B:
    # If you await a coroutine you schedule it for execution
    # (i.e., The file will be created)
    await coroutine_with_side_effects("z_awaiting_the_coroutine.txt")

    # C:
    # If you wrap a coroutine in a task, the wrapped coroutine is scheduled no
    # matter whether you await it or not
    # (i.e., The file will be created)
    asyncio.create_task(
        coroutine_with_side_effects("z_fire_and_forget_task.txt")
    )  # noqa: RUF006
    # Note that you need to give it some time, otherwise the task will never
    # get to be chosen by the event loop
    await asyncio.sleep(3)

    # D:
    # If you wrap a coroutine in a task, you get a handle that allows you to
    # interact with the task
    task_handle = asyncio.create_task(
        coroutine_with_side_effects("z_task_with_handle.txt"),
    )
    task_handle.add_done_callback(done_callback)
    await asyncio.sleep(2)

    # E:
    # Obviously, the cleaner ways is to also await the task
    task_handle = asyncio.create_task(
        coroutine_with_side_effects("z_awaited_task_with_handle.txt"),
    )
    task_handle.add_done_callback(done_callback)
    await task_handle


if __name__ == "__main__":
    # Start the event loop and schedule main()
    asyncio.run(main())
