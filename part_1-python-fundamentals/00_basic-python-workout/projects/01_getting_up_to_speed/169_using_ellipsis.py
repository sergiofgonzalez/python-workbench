"""Illustrate the use of ellipsis (...) in Python."""

from collections.abc import Callable
from functools import partial


def fn_stub() -> None:
    """Do nothing."""
    # Ellipsis can be used as a placeholder for future code (same as pass)
    ...  # noqa: PIE790


# Ellipsis can also be used in type hints, especially with tuples, etc.
def fn_with_ellipsis(param: tuple[int, ...]) -> None:
    """Accept a tuple of integers."""
    print(f"Received tuple with {len(param)} elements: {param}")


# Example of using ellipsis in type hints in Callable specifications
# This allows for flexible function signatures
# In this case, it accepts any number of positional arguments and keyword arguments
def fn_with_ellipsis_callable(a: int, b: int, sum_fn: Callable[..., int]) -> None:
    """Accept two integers and a function to compute their sum."""
    result = sum_fn(a, b)
    print(f"Sum of {a} and {b} is {result}")


def sum_function(x: int, y: int, label: str) -> int:
    """Return the sum of two integers."""
    """This function is just an example and will not be called in the main function."""
    print(f"Calculating sum of {x} and {y} with label: {label}")
    return x + y


def main() -> None:
    """Application entry point."""
    fn_with_ellipsis((1, 2, 3))
    try:
        fn_with_ellipsis(
            (1, 2, "a"),  # pyright: ignore[reportArgumentType]
        )  # This will raise a type error if type checking is enforced
    except TypeError as e:
        print(f"Type error: {e}")

    fn_with_ellipsis_callable(3, 5, lambda x, y: x + y)
    fn_with_ellipsis_callable(3, 5, partial(sum_function, label="Sum"))


if __name__ == "__main__":
    main()
