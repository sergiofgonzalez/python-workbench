"""A basic sync context manager."""

import asyncio

import aiofiles


class AsyncFile:
    """File Async Context Manager."""

    def __init__(self, file_name: str, method: str) -> None:
        """Construct File Context Manager instance."""
        self.file_name = file_name
        self.method = method
        self.file_obj = None

    async def __aenter__(self):
        """Perform the File object setup when entering the context manager."""
        self.file_obj = await aiofiles.open(self.file_name, self.method)
        return self.file_obj

    async def __aexit__(
        self, exc_type, exc_value, exc_traceback
    ) -> bool | None:
        """Perform the File object teardown when exiting the context manager."""
        if exc_value is not None:
            print(f"oops! an exception of type {type} occurred: {exc_value!r}")
            print("Exception handled: won't be propagated")
        await self.file_obj.close()
        # if you comment the following line the exception will be bubbled up
        return True


async def main() -> None:
    """Application entry point."""
    async with AsyncFile("my_file.txt", "w") as file:
        await file.write("Hello to Jason Isaacs!")

    async with AsyncFile("my_file.txt", "r") as file:
        await file.made_up_method("hello, hello!")


if __name__ == "__main__":
    asyncio.run(main())
