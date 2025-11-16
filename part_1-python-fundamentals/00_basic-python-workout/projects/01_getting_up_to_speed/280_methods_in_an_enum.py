"""Illustrate how to create regular class methods in an enum."""

from enum import Enum


class Direction(Enum):
    """Models the four cardinal directions as an enumeration."""

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def is_opposite(self, other: "Direction") -> bool:
        """Check if the given direction is opposite to the current one."""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.EAST: Direction.WEST,
            Direction.SOUTH: Direction.NORTH,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self] == other

    def __repr__(self) -> str:
        """Developer-friendly string representation of the Direction."""
        return f"<Direction.{self.name}: {self.value}>"

    def __str__(self) -> str:
        """User-friendly string representation of the Direction."""
        return f"{self.name} ({self.value})"


def move_to(direction: Direction, distance: float) -> None:
    """Move to the given direction."""
    print(f"Moving {distance} m on {direction} direction")

def main() -> None:
    """Application entry point."""
    move_to(Direction.NORTH, 10)
    move_to(Direction.EAST, 5)
    move_to(Direction.SOUTH, 2)
    move_to(Direction.WEST, 8)

    north = Direction.NORTH
    south = Direction.SOUTH
    if north.is_opposite(south):
        print(f"{north} is opposite to {south}")
    else:
        print(f"{north} is not opposite to {south}")
    print(f"Direction: {north}, Opposite: {south}")

    print(f"Developer representation: {north!r}")


if __name__ == "__main__":
    main()
