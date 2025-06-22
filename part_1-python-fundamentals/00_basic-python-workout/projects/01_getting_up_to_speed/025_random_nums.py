"""Generating random numbers with random lib."""

import random


def main() -> None:
    """Application entry point."""
    num = random.randint(0, 10)  # noqa: S311
    print("Random number between 0 and 10:", num)

    num = random.uniform(7.5, 10.5)  # noqa: S311
    print("Random float between 7.5 and 10.5:", num)


if __name__ == "__main__":
    main()
