"""Consuming a generator's iterator with next()."""

from collections.abc import Iterator


def generator_fn() -> Iterator[int]:
    """Return an iterator over the numbers from 0 to 2."""
    for i in range(3):
        yield i


gen = generator_fn()

print(next(gen))
print(next(gen))
print(next(gen))

# Oops!
print(next(gen))
