"""Using async queues to synchronize consumers and producers in asyncio."""

import asyncio
import itertools as it
import os
import random
import time


async def make_item(size: int = 5) -> str:
    """Return a random string of size chars long."""
    return os.urandom(size).hex()


async def rand_sleep(caller: str | None = None) -> None:
    """
    If called with something other than none sleep for a random number of
    seconds between 0 and 10.
    """
    i = random.randint(0, 10)
    if caller:
        print(f"{caller} sleeping for {i} second(s).")
    await asyncio.sleep(i)


async def produce(name: int, q: asyncio.Queue) -> None:
    """
    Add a random number of producers to a queue.

    The queue message is a random string of 5 characters.
    """
    n = random.randint(0, 10)
    for _ in it.repeat(None, n):
        await rand_sleep(caller=f"Producer {name}")
        i = await make_item()
        t = time.perf_counter()
        await q.put((i, t))
        print(f"Producer {name} added <{i}> to the queue.")


async def consume(name: int, q: asyncio.Queue) -> None:
    """Endlessly consume items from the queue."""
    while True:
        i, t = await q.get()
        now = time.perf_counter()
        print(
            f"Consumer {name} got element <{i}> from the queue in {now - t:0.5f} seconds."
        )
        q.task_done()


async def main(n_producers: int, n_consumers: int) -> None:
    """Create producers and consumers and start processing until done."""
    q = asyncio.Queue()
    producers = [asyncio.create_task(produce(n, q)) for n in range(n_producers)]
    consumers = [asyncio.create_task(consume(n, q)) for n in range(n_consumers)]
    await asyncio.gather(*producers)
    # Implicitly await consumers
    await q.join()
    for c in consumers:
        c.cancel()


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main(n_producers=5, n_consumers=10))
    elapsed = time.perf_counter() - start
    print(f"Program completed in {elapsed:0.3f} seconds.")
