"""Illustrates how to implement an asynchronous context manager using asyncio."""

import asyncio
from pathlib import Path
from typing import TYPE_CHECKING

import aiofiles

if TYPE_CHECKING:
    from types import TracebackType

base_path = Path("data", "out_data", "tmp")


class AsyncFileManager:
    """Asynchronous context manager for file operations."""

    def __init__(self, filename: str, mode: str) -> None:
        """Initialize with filename and mode."""
        self.filename = filename
        self.mode = mode
        self.file = None

    async def __aenter__(self) -> aiofiles.threadpool.text.AsyncTextIOWrapper:
        """Enter the asynchronous context and open the file."""
        self.file = await aiofiles.open(self.filename, self.mode)
        return self.file

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Exit the asynchronous context and close the file."""
        if exc_type is not None:
            print(f"__aexit__: Exception received: {exc_value} (type: {exc_type})")
            print(f"__aexit__: Traceback: {traceback}")
            print("__aexit__: Exceptions other than IOError are not handled.")
            if issubclass(exc_type, IOError):
                print("__aexit__: Suppressing IOError exception.")
                return True  # Suppress IOError exceptions
        await self.file.close()  # ty:ignore[possibly-missing-attribute]
        return None


async def main() -> None:
    """Asynchronous application entry point."""
    file_path = base_path / "example.txt"

    async with AsyncFileManager(file_path.as_posix(), "w") as file:
        await file.write("Hello to Jason Isaacs!")  # ty:ignore[unresolved-attribute]

    try:
        async with AsyncFileManager(file_path.as_posix(), "r") as file:
            await file.made_up_method("hello, hello!")  # ty:ignore[unresolved-attribute]
    except AttributeError as e:
        print(f"Caught an AttributeError bubbled up from __aexit__: {e}")

    async with AsyncFileManager(file_path.as_posix(), "r") as file:
        contents = await file.read()  # ty:ignore[unresolved-attribute]
    print("File contents:", contents)


if __name__ == "__main__":
    # Start the event loop on the current thread and schedule main() to run.
    asyncio.run(main())
