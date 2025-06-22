"""Illustrate how to use user-defined libraries in Python."""

from my_lib import greet_me, square


def main() -> None:
    """Application entry point."""
    name = "Alice"
    greet_me(name)

    number = 5
    result = square(number)
    print(f"The square of {number} is {result}.")


if __name__ == "__main__":
    main()
