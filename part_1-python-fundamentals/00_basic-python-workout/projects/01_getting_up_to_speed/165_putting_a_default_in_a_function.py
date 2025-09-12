"""Partial for default values in functions.

Illustrate how to use partial to put a default value in a function that
doesn't have one.
"""
from functools import partial

square = partial(pow, exp=2)


def main() -> None:
    """Application entry point."""
    """Example usage of the partial function."""
    print(f"Square of 3: {square(3)}")
    print(f"Square of 4: {square(4)}")
    print(f"Square of 5: {square(5)}")

if __name__ == "__main__":
    main()
