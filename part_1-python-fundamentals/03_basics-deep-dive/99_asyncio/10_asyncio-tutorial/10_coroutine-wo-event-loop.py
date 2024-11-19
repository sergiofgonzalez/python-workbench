"""Invoking a coroutine not tied to an event loop doesn't do anything."""

from pathlib import Path


async def main() -> None:
    """Write a file in a current dir as an indicator."""
    with Path.open("running.txt", "w") as file:
        file.write("Hello from a coroutine!")


if __name__ == "__main__":
    # nothing happens
    main()
