"""Illustrate Python's module search path."""

import sys

from mymath import area  # ty:ignore[unresolved-import]


def main() -> None:
    """Display the area of a circle with radius 5."""
    print("Python module search path:")
    for path in sys.path:
        print(f"- {path}")

    # sys.path[0] is the directory containing the script that was used to invoke
    #  the Python interpreter.
    print(f"\nThe first entry in sys.path is: {sys.path[0]}")

    radius = 5
    circle_area = area(radius)
    print(f"The area of a circle with radius {radius} is {circle_area}")


if __name__ == "__main__":
    main()
