"""Illustrate how to exit a program by raising a SystemExit."""

import sys
from random import randint


def main() -> None:
    """Application entry point."""
    while True:
        result = randint(1, 6)  # noqa: S311
        if result % 2 == 0:
            print(f"You rolled {result}, which is even.")
        else:
            print(f"You rolled {result}, which is odd. Exiting with a SystemExit.")
            msg = f"Exiting the program after rolling an odd number: {result}"
            raise SystemExit(msg)


if __name__ == "__main__":
    main()
