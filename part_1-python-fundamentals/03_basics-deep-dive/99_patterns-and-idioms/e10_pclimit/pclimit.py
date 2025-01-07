"""PCLimit.

Async context manager to run async code with limited parallel concurrency.
"""

import asyncio
import types

from loguru import logger

# Uncomment should the library be released
logger.disable(__name__)  # noqa: ERA001


class WorkerError(Exception):
    """Exception raised from a worker."""


class PCLimit:
    """Async context manager to run async code with limited parallel concurrency."""

    def __init__(
        self,
        *,
        concurrency: int = 2,
        fail_on_worker_errors: bool = True,
    ) -> None:
        """Initialize an instance of the PCLimit Context Manager."""
        self._concurrency = concurrency
        self._work_queue = asyncio.Queue()
        self._consumer_tasks = []
        self._fail_on_worker_errors = fail_on_worker_errors
        self._worker_error = None

    @property
    def concurrency(self) -> int:
        """Concurrency getter."""
        return self._concurrency

    async def __aenter__(self) -> "PCLimit":
        """Set up the resources to manage async code with limited concurrency."""
        self._consumer_tasks = [
            asyncio.create_task(self._spin_up_async_worker(f"worker-{i}"))
            for i in range(self.concurrency)
        ]
        return self

    async def _spin_up_async_worker(self, worker_name: str) -> None:
        """Infinite loop where a worker gets item from the work queue and process it."""
        while True:
            logger.info(
                "{worker_name} is ready and waiting for work",
                worker_name=worker_name,
            )
            future, fn, args, kwargs = await self._work_queue.get()
            logger.info("{worker_name} is working", worker_name=worker_name)
            try:
                result = await fn(*args, **kwargs)
            except Exception as e:
                future.set_exception(e)
                self._work_queue.task_done()
                msg = f"worker failed with exception {type(e)}({e})"
                self._worker_error = WorkerError(msg)
                if self._fail_on_worker_errors:
                    logger.error(
                        "worker related exception: {worker_name}: {e}",
                        worker_name=worker_name,
                        e=e,
                    )
                    raise self._worker_error from e
                logger.warning(f"worker related exception (will continue): {e}", e=e)
            else:
                future.set_result(result)
                self._work_queue.task_done()

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: types.TracebackType | None,
    ) -> None:
        """Tear down the resources to manage async code with limited concurrency."""
        await self._work_queue.join()
        self._work_queue = None
        for task in self._consumer_tasks:
            task.cancel()
        if exc_value is not None:
            logger.error(
                "async context manager exception occurred: {exc_value} ({exc_type})",
            )
            raise exc_value
        if self._worker_error and self._fail_on_worker_errors:
            raise self._worker_error

    async def _enqueue_work(
        self,
        fn: types.CoroutineType,
        *args: any,
        **kwargs: any,
    ) -> asyncio.Future:
        """Put the fn and args to be called by the worker in a queue."""
        future = asyncio.Future()
        await self._work_queue.put((future, fn, args, kwargs))
        return future

    async def run(
        self,
        fn: types.CoroutineType,
        *args: any,
        **kwargs: any,
    ) -> asyncio.Future:
        """Return the Future returned by calling fn(*args, **kwargs)."""
        if not asyncio.iscoroutinefunction(fn):
            msg = "fn must be a coroutine function"
            raise ValueError(msg)
        call_fn_task = asyncio.create_task(self._enqueue_work(fn, *args, **kwargs))
        call_fn_result_future = await call_fn_task
        return call_fn_result_future  # noqa: RET504
