"""Using dequeue (double-ended queue, pronounced "deck") for FIFO operations."""

from collections import deque
from time import perf_counter
from timeit import timeit


def time_fifo_operations(n: int) -> None:
    """Time FIFO operations using a deque."""
    # First with a regular queue
    my_list = list(range(n))
    list_start_ts = perf_counter()
    for _ in range(n):
        my_list.pop(0)
    list_end_ts = perf_counter()
    list_exec_time = list_end_ts - list_start_ts
    # Now with a dequeue
    my_dequeue = deque(range(n))
    dequeue_start_ts = perf_counter()
    for _ in range(n):
        my_dequeue.popleft()
    dequeue_end_ts = perf_counter()
    dequeue_exec_time = dequeue_end_ts - dequeue_start_ts

    print(
        f"{n:<8,} {'list:':<8} {list_exec_time:>10.6f} "
        f"| {'dequeue:':<8} {dequeue_exec_time:>10.6f}",
    )


def timeit_fifo_operations(n: int) -> None:
    """Time FIFO operations using a deque using timeit."""
    my_list = list(range(n))
    my_deque = deque(range(n))
    exec_time_list = timeit(stmt=lambda: my_list.pop(0), number=n)
    exec_time_deque = timeit(stmt=lambda: my_deque.popleft(), number=n)

    print(
        f"{n:<8,} {'list:':<8} {exec_time_list:>10.6f} "
        f"| {'dequeue:':<8} {exec_time_deque:>10.6f}",
    )


def main() -> None:
    """Application entry point."""
    for num_items in (100, 1_000, 10_000, 100_000):
        time_fifo_operations(num_items)
    print("=== with timeit ===")
    for num_items in (100, 1_000, 10_000, 100_000):
        timeit_fifo_operations(num_items)


if __name__ == "__main__":
    main()
