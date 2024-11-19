"""Explores the similarities between generators and coroutines."""

import asyncio
import random
from collections.abc import Generator


def make_randoms(n: int) -> Generator[int, None, None]:
    """Generate n random ints."""
    for _ in range(n):
        yield random.randint(0, 10)


async def greeting(name: str) -> str:
    """Coroutine that return a greeting."""
    return f"Hello, {name}!"


async def main() -> None:
    """Application entry point."""
    gen = make_randoms(5)
    print(f"{type(gen)}")

    coro = greeting("Jason Isaacs")
    print(f"{type(coro)}")

    # both a generator and coroutine look similar in terms of: when invoking
    # them, they return an object rather than the result of calling the function

    # To obtain the result of the generator you need to use next()
    print(f"{next(gen)=}")

    # To obtain the result of a coroutine, you need to await it
    print(await greeting("Florence Pugh"))


if __name__ == "__main__":
    asyncio.run(main())
