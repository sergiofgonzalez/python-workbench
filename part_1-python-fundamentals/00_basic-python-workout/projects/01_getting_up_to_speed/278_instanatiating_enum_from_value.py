"""Illustrates how to instantiate an enum from a value."""

from enum import Enum


class Direction(Enum):
    """Models the four cardinal directions as an enumeration."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


def main() -> None:
    """Application entry point."""
    south = Direction(2)
    print(f"{isinstance(south, Direction)=}")
    print(f"{south.name=}, {south.value=}")
    assert south == Direction.SOUTH

    # try to instantiate with an invalid value
    try:
        _ = Direction(5)
    except ValueError as e:
        print(f"Caught expected exception: {e}")

    # You can also instantiate using the name
    east = Direction["EAST"]
    print(f"{isinstance(east, Direction)=}")
    print(f"{east.name=}, {east.value=}")
    assert east == Direction.EAST


if __name__ == "__main__":
    main()
