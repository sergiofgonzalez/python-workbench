"""Illustrate how to import libs from folders and current dir."""

from my_lib import greet_me, square
from utils.my_lib import cube


def main() -> None:
    """Application entry point."""
    name = "Alice"
    greet_me(name)

    number = 5
    result = square(number)
    print(f"The square of {number} is {result}.")

    number = 3
    result = cube(number)
    print(f"The cube of {number} is {result}.")


if __name__ == "__main__":
    main()
