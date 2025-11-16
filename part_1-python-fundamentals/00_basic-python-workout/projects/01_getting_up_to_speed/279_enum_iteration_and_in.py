"""Illustrates how to iterate over an enum and access its members securely."""

from enum import Enum


class Direction(Enum):
    """Models the four cardinal directions as an enumeration."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def main() -> None:
    """Application entry point."""
    directions = list(Direction)
    print(f"All directions: {directions}")

    for direction in Direction:
        print(f"Direction: {direction.name}, Value: {direction.value}")

    print(f"First direction: {directions[0]}")
    print(f"Last direction: {directions[-1]}")

    if 4 in Direction:  # noqa: PLR2004
        print("Direction with value 4 exists.")
    else:
        print("Direction with value 4 does not exist.")

    if 2 in Direction:  # noqa: PLR2004
        print("Direction with value 2 exists.")
    else:
        print("Direction with value 2 does not exist.")


if __name__ == "__main__":
    main()
