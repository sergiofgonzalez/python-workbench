"""Illustrates the basics of using aiofiles with asyncio."""

import asyncio
import string
from datetime import UTC, datetime
from pathlib import Path
from random import choice
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from collections.abc import Callable

base_path = Path("data", "out_data", "tmp")


async def async_write_lines(filename: str) -> None:
    """Asynchronously write multiple lines to a file."""
    async with aiofiles.open(filename, mode="a") as file:
        choices = string.ascii_letters + string.digits
        for i in range(1000):
            random_str = "".join(choice(choices) for _ in range(40))  # noqa: S311
            print(f"Writing line {i + 1}")
            await file.write(f"Line {i + 1}: {random_str}\n")


async def print_current_time(label: str) -> None:
    """Print the current time with msecs."""
    while True:
        print(
            f"{label}: {datetime.now(tz=UTC).strftime('%H:%M:%S.%f')}",
        )
        await asyncio.sleep(0)  # yield control to event loop


def make_done_callback(
    clock_task: asyncio.Task[None],
) -> Callable[[asyncio.Task[None]], None]:
    """Create a done callback that cancels the clock task."""

    def writing_done_cb(_: asyncio.Task[None]) -> None:
        """Cancel clock_task when writing is done."""
        print("Asynchronous writing completed.")
        clock_task.cancel()

    return writing_done_cb


async def main() -> None:
    """Async application entry point."""
    file_path = base_path / "hello_aiofiles.txt"

    # Writing to a file asynchronously
    async with aiofiles.open(file_path.as_posix(), mode="w") as file:
        await file.write("Hello, aiofiles with asyncio!\n")
        await file.write("This is an example of asynchronous file I/O.\n")
        await file.write("Goodbye!\n")
    print(f"Wrote to {file_path}")
    print("=" * 40)

    # Reading from a file asynchronously (in one shot)
    async with aiofiles.open(file_path.as_posix()) as file:
        contents = await file.read()

    # contents are avaible outside of the async with block
    print(f"Contents of {file_path}:")
    print(contents)
    print("=" * 40)

    # Reading from a file asynchronously (line by line)
    async with aiofiles.open(file_path.as_posix()) as file:
        print(f"Reading {file_path} line by line:")
        async for line in file:
            print(f"> {line.strip()}")
    print("=" * 40)

    # To confirm that aiofiles operates in non-blocking fashion,
    # we can add some other concurrent async operations in parallel
    # and we will see them progress cooperatively.
    clock_task = asyncio.create_task(print_current_time("Clock"))
    async_write_task = asyncio.create_task(async_write_lines(file_path.as_posix()))

    # When async_write_task is done, cancel the clock_task
    # Becaus the callback is a sync function that only receives the completed task,
    # we use a closure to make clock_task available to the callback so that it can
    # cancel it.
    async_write_task.add_done_callback(make_done_callback(clock_task))

    # Wait for both tasks to complete (clock_task will be cancelled by callback)
    await asyncio.gather(async_write_task, clock_task, return_exceptions=True)


if __name__ == "__main__":
    # start the event loop in the current thread and schedule main() to run.
    asyncio.run(main())
