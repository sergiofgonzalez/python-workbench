# WorkQueue and `asyncio.Queue`

Use the `WorkQueue` class to classify a large list of number into even and odd categories.

## main_v0

Using directly `asyncio.Queue`. Because the classification task is not I/O, we can see that workers do not pick up items from the queue, so increasing the number of workers do not help with the execution time (Process took 0.928857 seconds).

## main_v1

Using directly `asyncio.Queue`. Because the classification task is not I/O we use to_thread. Now we have different workers in place, so increasing the concurrency helps with the total execution time (Process took 0.903563 seconds).

## main_v2

Using directly `asyncio.Queue` and `asyncio.sleep()` so that more workers get into the mix. However, `asyncio.sleep()` is slow (Process took 2.307211 seconds).

## main_v3

Using the `WorkQueue` for better DX, but we see that the execution is much slower.