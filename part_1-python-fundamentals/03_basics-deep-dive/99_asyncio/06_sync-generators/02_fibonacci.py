"""Generator that provides the numbers of the Fibonacci sequence."""

from collections.abc import Iterator


def fibonacci(n: int) -> Iterator[int]:
    """Return an iterator over the first n numbers of the Fibonacci sequence."""
    a = 1
    b = 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# Print the first 10 numbers of the Fibonacci sequence
for i in fibonacci(10):
    print(i)


# non-generator based impl
def get_fibon_seq(n: int) -> list[int]:
    """Return a list with the first n numbers of the Fibonacci sequence."""
    nums = []
    a = 1
    b = 1
    for _ in range(n):
        nums.append(a)
        a, b = b, a + b
    return nums


for i in get_fibon_seq(10):
    print(i)
