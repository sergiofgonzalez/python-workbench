"""Illustrate the use of closures in Python."""

from collections.abc import Callable


def make_power_fn(power: int) -> Callable[[int], int]:
    """Return a function that raises a number to the given power."""

    def power_fn(x: int) -> int:
        """Raise x to the specified power."""
        return x**power

    return power_fn


def increment_maker(increment: int) -> Callable[[int], int]:
    """Return a function that increments a number by the given value."""

    def increment_fn(x: int) -> int:
        """Increment x by the specified value."""
        return x + increment

    return increment_fn


def main() -> None:
    """Application entry point."""
    square = make_power_fn(2)
    cube = make_power_fn(3)

    assert square(4) == 16, "4 squared should be 16"  # noqa: PLR2004
    assert cube(3) == 27, "3 cubed should be 27"  # noqa: PLR2004

    print(f"Square of 4: {square(4)}")
    print(f"Cube of 3: {cube(3)}")

    increment_by_5 = increment_maker(5)
    increment_by_10 = increment_maker(10)
    assert increment_by_5(10) == 15, "10 incremented by 5 should be 15"  # noqa: PLR2004
    assert increment_by_10(10) == 20, "10 incremented by 10 should be 20"  # noqa: PLR2004

    print(f"10 incremented by 5: {increment_by_5(10)}")
    print(f"10 incremented by 10: {increment_by_10(10)}")


if __name__ == "__main__":
    main()
