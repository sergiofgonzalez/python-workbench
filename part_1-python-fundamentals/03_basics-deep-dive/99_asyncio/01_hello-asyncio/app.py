"""A basic asyncio program."""

import asyncio


async def counter(name: str) -> None:
    """
    Print the numbers from 0 to 100 in an async fashion, yielding control to
    the event loop in each iteration so that other tasks can run concurrently.
    """
    for i in range(100):
        print(f"{name}: {i!s}")
        # Yield control to the event loop so that something else can run
        await asyncio.sleep(0)


async def main() -> None:
    """Set up 4 async tasks and run them until all of them  finished."""
    tasks = [asyncio.create_task(counter(f"Task{n}")) for n in range(4)]

    while True:
        tasks = [t for t in tasks if not t.done()]
        if len(tasks) == 0:
            return
        # If there are pending tasks, execute them
        await tasks[0]


if __name__ == "__main__":
    # Run the main() coroutine object, and return the result, starting new event
    # loop for the current thread (if there's already an event loop this will
    # fail).
    asyncio.run(main())
