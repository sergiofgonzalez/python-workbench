"""Illustrate how to consume the mymath module."""

import mymath
from mymath import pi


def main() -> None:
    """Application entry point."""
    circle_area = mymath.area(5.0)
    print(f"The area of a circle with radius 5.0 is {circle_area:.2f}")
    print(f"Value of pi from mymath module is {pi}")


if __name__ == "__main__":
    main()
