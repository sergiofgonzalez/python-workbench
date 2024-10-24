"""A basic sync context manager."""

import asyncio
from contextlib import asynccontextmanager

import aiofiles


@asynccontextmanager
async def async_open_file(file_name, method):
    """Async context manager implemented as a generator."""
    async_file_obj = await aiofiles.open(file_name, method)
    try:
        yield async_file_obj
    except Exception as e:
        print(f"oops! an exception of type {type(e)} occurred: {e!r}")
        print("Exception handled: won't be propagated")
    finally:
        await async_file_obj.close()



async def main() -> None:
    """Application entry point."""
    async with async_open_file("my_file.txt", "w") as file:
        await file.write("Hello to Jason Isaacs!")

    async with async_open_file("my_file.txt", "r") as file:
        await file.made_up_method("hello, hello!")


if __name__ == "__main__":
    asyncio.run(main())
