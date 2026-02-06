"""Illustrates that invoking a coroutine doesn't execute it."""

import asyncio


async def coro() -> str:
    """Return a greeting after a short delay."""
    await asyncio.sleep(1)
    return "Hello, World!"


async def main() -> None:
    """Async application entry point."""
    greeting_coro = coro()
    print(f"Invoked coro(), got: {greeting_coro}")
    print("Note that the coroutine has not executed yet.")
    print("=" * 40)

    # to execute it, you need to await it
    greeting = await greeting_coro
    print(f"After awaiting, got greeting: {greeting}")

if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main())
