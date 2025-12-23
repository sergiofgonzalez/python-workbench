"""Consumes the mymath module via 'from module import name1, name2'."""

from mymath import area


def main() -> None:
    """Application entry point."""
    radius = 5
    circle_area = area(radius)
    print(f"The area of a circle with radius {radius} is {circle_area}")


if __name__ == "__main__":
    main()
