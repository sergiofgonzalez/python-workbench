"""Illustrate how to exit a program with `sys.exit()` which doesn't work in notebooks."""

import sys
from random import randint


def main() -> None:
    """Application entry point."""
    while True:
        result = randint(1, 6)  # noqa: S311
        if result % 2 == 0:
            print(f"You rolled {result}, which is even.")
        else:
            print(f"You rolled {result}, which is odd. Exiting with sys.exit().")
            sys.exit()


if __name__ == "__main__":
    main()
