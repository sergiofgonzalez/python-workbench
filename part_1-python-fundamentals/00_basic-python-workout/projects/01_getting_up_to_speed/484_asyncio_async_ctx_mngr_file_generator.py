"""Illustrates how to implement an asynchronous context manager using a generator."""

import asyncio
from contextlib import asynccontextmanager
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

base_path = Path("data", "out_data", "tmp")


@asynccontextmanager
async def async_file_manager(
    filename: str,
    mode: str,
) -> AsyncGenerator[aiofiles.threadpool.text.AsyncTextIOWrapper]:
    """Asynchronous context manager for file operations using a generator."""
    file = await aiofiles.open(filename, mode)
    try:
        yield file
    except Exception as exc:
        print(f"async_file_manager: Exception received: {exc} (type: {type(exc)})")
        print("async_file_manager: Exceptions other than IOError are not handled.")
        if isinstance(exc, IOError):
            print("async_file_manager: Suppressing IOError exception.")
            return  # Suppress IOError exceptions
        raise
    finally:
        await file.close()


async def main() -> None:
    """Asynchronous application entry point."""
    file_path = base_path / "example.txt"

    async with async_file_manager(file_path.as_posix(), "w") as file:
        await file.write("Hello to Jason Isaacs!")  # ty:ignore[unresolved-attribute]

    try:
        async with async_file_manager(file_path.as_posix(), "r") as file:
            await file.made_up_method("hello, hello!")  # ty:ignore[unresolved-attribute]
    except AttributeError as e:
        print(f"Caught an AttributeError bubbled up from __aexit__: {e}")

    async with async_file_manager(file_path.as_posix(), "r") as file:
        contents = await file.read()  # ty:ignore[unresolved-attribute]
    print("File contents:", contents)


if __name__ == "__main__":
    # Start the event loop on the current thread and schedule main() to run.
    asyncio.run(main())
