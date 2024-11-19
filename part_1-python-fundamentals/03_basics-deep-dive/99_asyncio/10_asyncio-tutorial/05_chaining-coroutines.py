"""TBD."""

import asyncio
import random
import time

from rich import print


async def part1(n: int) -> str:
    """
    Sleep for a random number of seconds between 0 and 10 and return the string
    "result{n}-1", with `n` being the argument passed to the function.
    """
    i = random.randint(0, 10)
    print(f"[color({n})]part1({n}): sleeping for {i} seconds.[/color({n})]")
    await asyncio.sleep(i)
    result = f"result{n}-1"
    print(f"[color({n})]Returning part1({n}) -> {result}[color({n})]")
    return result


async def part2(n: int, arg: str) -> str:
    """
    Sleep for a random number of seconds between 0 and 10 and return the string
    "result{n}-2 derived from {arg}", with `n` and `arg` being the arguments
    passed to the function.
    """
    i = random.randint(0, 10)
    print(
        f"[color({n})]part2({n}, {arg}): sleeping for {i} seconds.[/color({n})]",  # noqa: E501
    )
    await asyncio.sleep(i)
    result = f"result{n}-2 derived from {arg}"
    print(f"[color({n})]Returning part2({n}, {arg}) -> {result}.[/color({n})]")
    return result


async def chain(n: int) -> None:
    """
    Execute the chaining of part1() and part2(), that is part2(part1())
    asynchronously.
    """
    start = time.perf_counter()
    p1 = await part1(n)
    p2 = await part2(n, p1)
    end = time.perf_counter() - start
    print(
        f"[color({n})]>>> chained result{n}: {p2} (took: {end:0.3f} sec).[/color({n})]",  # noqa: E501
    )


async def main(*args: int) -> None:
    """Run a variable number of chain() asynchronously."""
    await asyncio.gather(*(chain(n) for n in args))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main(1, 2, 3))
    end = time.perf_counter() - start
    print(f"Program finished in {end:0.3f} seconds.")
