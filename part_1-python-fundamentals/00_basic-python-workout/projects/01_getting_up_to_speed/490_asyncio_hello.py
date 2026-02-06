"""TODO: description of the program."""

import asyncio


async def main() -> None:
    """Async application entry point."""
    await asyncio.sleep(1)
    print("Hello, Asyncio!")


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())  # blocks the execution until main() is complete
    print("Hello, back!")
