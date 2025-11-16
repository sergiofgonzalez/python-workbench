"""Introduces the concept of enumeration in Python."""

from enum import Enum


class Direction:
    """Models the four cardinal directions as a regular class with static properties."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class DirectionV2(Enum):
    """Models the four cardinal directions as an enumeration."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class DirectionV3(Enum):
    """Models the four cardinal directions as a string enumeration."""

    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


def move_to(direction: Direction, distance: float) -> None:
    """Move to the given direction."""
    print(f">>> {isinstance(direction, int)=}")
    print(f">>> {isinstance(direction, Direction)=}")
    print(f"Moving {distance} m on {direction} direction")


def move_to_v2(direction: DirectionV2, distance: float) -> None:
    """Move to the given direction."""
    print(f">>> {isinstance(direction, DirectionV2)=}")
    print(f"Moving {distance} m on {direction.name} ({direction.value}) direction")


def move_to_v3(direction: DirectionV3, distance: float) -> None:
    """Move to the given direction."""
    print(f">>> {isinstance(direction, DirectionV3)=}")
    print(f"Moving {distance} m on {direction.name} ({direction.value}) direction")


def main() -> None:
    """Application entry point."""
    # using regular class direction is a poorly typed solution, but it works
    south = Direction.SOUTH
    move_to(south, 100)  # type: ignore  # noqa: PGH003
    move_to(2, 100)  # type: ignore  # noqa: PGH003
    print("=" * 20)

    # using enum is much better from the typing perspective, but you must be
    # aware of some nuances
    east = DirectionV2.EAST
    move_to_v2(east, 1_000)

    # You can iterate over the values of the enum
    for direction in DirectionV2:
        print(f"Direction: {direction.name}, Value: {direction.value}")
    print("=" * 20)

    # using string enum is exactly the same
    north = DirectionV3.NORTH
    move_to_v3(north, 10_000)

    assert north.name == "NORTH"
    assert north.value == "N"
    print("=" * 20)


if __name__ == "__main__":
    main()
