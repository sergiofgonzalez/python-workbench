"""WorkQueue with limited parallel execution using producers/consumers pattern."""

import asyncio
from collections.abc import Callable, Coroutine


class WorkQueue:
    """Queue in which you can put work to be processed asynchronously by consumers."""

    def __init__(self, concurrency: int) -> None:
        """Initialize the WorkQueue with the given number of consumers."""
        if not isinstance(concurrency, int):
            msg = "concurrency must be an integer"
            raise TypeError(msg)
        if concurrency <= 0:
            msg = "concurrency must be positive"
            raise ValueError(msg)

        self.work_queue = asyncio.Queue()
        self.consumer_tasks = []

        # spawn the consumers
        for _ in range(concurrency):
            task = asyncio.create_task(self.__consumer())
            self.consumer_tasks.append(task)

    async def __consumer(self) -> None:
        """Spin up a consumer that is constantly pulling work from the work queue.

        Because work items pulled from the queue are coroutine functions, work can
        be processed by simply awaiting the result of invoking the function.
        """
        while True:
            work_item = await self.work_queue.get()
            await work_item()
            self.work_queue.task_done()

    def put_work_item(self, work_item: Callable[[], Coroutine[any, any, any]]) -> None:
        """Append a work item to the work queue to be processed by the consumer group.

        The work_item must be a coroutine function, that is, a function that when it is
        invoked returns a coroutine object.
        """
        if not asyncio.iscoroutinefunction(work_item):
            msg = "the work item must be coroutine function"
            raise ValueError(msg)
        self.work_queue.put_nowait(work_item)

    async def until_all_work_done(self) -> None:
        """Wait until queue is empty and then perform clean-up of consumers.

        The cleanup consists of cancelling the tasks that wrap the coroutines that
        represent the consumer, and then waiting for those tasks to be done.
        """
        await self.work_queue.join()
        for task in self.consumer_tasks:
            task.cancel()

        await asyncio.gather(*self.consumer_tasks, return_exceptions=True)
