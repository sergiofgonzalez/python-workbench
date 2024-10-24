"""The simplest generator ever."""

from collections.abc import Iterator


def generator_fn() -> Iterator[int]:
    """Return an iterator over the numbers from 0 to 9."""
    for i in range(10):
        yield i


for item in generator_fn():
    print(item)
