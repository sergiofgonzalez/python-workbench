"""Illustrate how to annotate complex types."""

from collections.abc import Callable


def my_fun(nums: list[float]) -> Callable[[int, bool], str]:
    """Return a function that processes an integer and a boolean.

    Args:
        nums (list[float]): A list of floats.

    Returns:
        Callable[[int, bool], str]: A function that takes an integer and a boolean,
        returning a string.

    """

    def inner_function(x: int, y: bool) -> str:  # noqa: FBT001
        return f"Received {x} and {y} with list {nums}"

    return inner_function


def main() -> None:
    """Application entry point."""


if __name__ == "__main__":
    main()
