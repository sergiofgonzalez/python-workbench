"""A WorkQueue implementation in which you can check the result of individual tasks."""

import asyncio
import random
import time
from collections.abc import Callable, Coroutine


class WorkQueue:
    """An object to handle limited parallel concurrency with async code."""

    def __init__(self, concurrency: int = 2) -> None:
        """Initialize a WorkQueue instance with the desired parallel concurrency."""
        self._work_queue = asyncio.Queue()
        self._consumer_tasks = []
        for i in range(concurrency):
            task = asyncio.create_task(self._spin_up_consumer(f"worker-{i}"))
            self._consumer_tasks.append(task)

    async def _spin_up_consumer(self, name: str) -> None:
        print(f">> Spinning up {name}")
        while True:
            # print(f">> {name} is waiting for work")
            future, work_item = await self._work_queue.get()
            # print(f">> {name} is working")
            # process work_item here
            result = await work_item()
            future.set_result(result)
            self._work_queue.task_done()

    async def _enqueue_work(
        self,
        work_item: Callable[[], Coroutine[any, any, any]],
    ) -> asyncio.Future:
        future = asyncio.Future()
        # yields control to the event loop so that other things can progress
        await self._work_queue.put((future, work_item))
        return future

    async def run_work(
        self,
        work_item: Callable[[], Coroutine[any, any, any]],
    ) -> asyncio.Future:
        """Run a work item asynchronously returning a Future to get the result."""
        task = asyncio.create_task(self._enqueue_work(work_item))
        work_item_result_future = await task
        return work_item_result_future  # noqa: RET504

    async def until_work_done(self) -> None:
        """Tear down the resources associated to the WorkQueue."""
        await self._work_queue.join()
        self._work_queue = None
        for t in self._consumer_tasks:
            t.cancel()
        await asyncio.gather(*self._consumer_tasks, return_exceptions=True)


async def async_work() -> float:
    """Async piece of work to be handled by WorkQueue (as an example)."""
    delay_seconds = random.uniform(0.5, 1.5)  # noqa: S311
    await asyncio.sleep(delay_seconds)
    return delay_seconds


async def main() -> None:
    """Async application entry point."""
    work_queue = WorkQueue(concurrency=3)
    futures = []
    start = time.perf_counter()
    for _ in range(10):
        future = await work_queue.run_work(async_work)
        futures.append(future)
    await asyncio.gather(*futures)
    real_sleep_time = time.perf_counter() - start
    total_requested_sleep_time = 0
    for i, f in enumerate(futures):
        print(f"{i}: {f.result()=}")
        total_requested_sleep_time += f.result()

    print(f"Requested sleep time: {total_requested_sleep_time:.3f}")
    print(f"Real sleep time: {real_sleep_time:.3f}")
    print(f"{real_sleep_time / total_requested_sleep_time:.3f}")


if __name__ == "__main__":
    asyncio.run(main())
