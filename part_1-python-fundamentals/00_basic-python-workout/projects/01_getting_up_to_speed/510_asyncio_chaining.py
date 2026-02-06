"""Illustrates the concept of chaining async functions together."""

import asyncio
import random
import time

import rich


async def big_process(n: int) -> str:
    """Simulate a big async process consisting of multiple steps."""
    task_name = f"big_process({n})"
    delay1 = random.randint(0, 10)  # noqa: S311
    rich.print(
        f"[color({n})]{task_name} starting big_process({n}) with delay1={delay1}[/color({n})]",  # noqa: E501
    )
    await asyncio.sleep(delay1)
    delay2 = random.randint(0, 10)  # noqa: S311
    rich.print(
        f"[color({n})]{task_name} continuing big_process({n}) with delay2={delay2}[/color({n})]",  # noqa: E501
    )
    await asyncio.sleep(delay2)
    rich.print(f"[color({n})]{task_name} done: returning[/color({n})]")
    result = f"result: {n} ({delay1} + {delay2} seconds)"
    return result  # noqa: RET504


async def process_part1(n: int) -> str:
    """Simulate part 1 of a big process."""
    delay = random.randint(0, 10)  # noqa: S311
    rich.print(f"[color({n})]process_part1({n}) sleeping for {delay}[/color({n})]")
    await asyncio.sleep(delay)
    rich.print(f"[color({n})]process_part1({n}) done[/color({n})]")
    return f"part1 result: {n} ({delay} seconds)"


async def process_part2(n: int) -> str:
    """Simulate part 2 of a big process."""
    delay = random.randint(0, 10)  # noqa: S311
    rich.print(f"[color({n})]process_part2({n}) sleeping for {delay}[/color({n})]")
    await asyncio.sleep(delay)
    rich.print(f"[color({n})]process_part2({n}) done[/color({n})]")
    return f"part2 result: {n} ({delay} seconds)"


async def chain_process(n: int) -> str:
    """Chain multiple async processes together."""
    part1_result = await process_part1(n)
    part2_result = await process_part2(n)
    final_result = f"chain_process({n}) results: {part1_result} + {part2_result}"
    rich.print(f"[color({n})]{final_result}[/color({n})]")
    return final_result


async def main(*args: int) -> None:
    """Async application entry point."""
    # Lab 1: invoking big_process with asyncio.gather
    start_time = time.perf_counter()
    results = await asyncio.gather(*(big_process(n) for n in args))
    print(results)
    print(
        f"Lab 1: parallel check (gather()): {time.perf_counter() - start_time:.3f} seconds",  # noqa: E501
    )
    print("=" * 40)
    # Lab 2: invoking chain_process with asyncio.gather
    start_time = time.perf_counter()
    results = await asyncio.gather(*(chain_process(n) for n in args))
    print(results)
    print(
        f"Lab 2: parallel check (gather()): {time.perf_counter() - start_time:.3f} seconds",  # noqa: E501
    )
    print("=" * 40)


if __name__ == "__main__":
    # start the evt loop in the current thread and schedule main() to run.
    asyncio.run(main(1, 2, 3))
