"""The basics of operator overloading."""


class Rectangle:
    """A class representing a rectangle."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize the rectangle with width and height."""
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self.width * self.height

    def scale(self, factor: float) -> "Rectangle":
        """Return a new Rectangle scaled by a given factor."""
        if factor <= 0:
            msg = "Scale factor must be positive."
            raise ValueError(msg)
        return Rectangle(
            width=self.width * factor,
            height=self.height * factor,
        )

    # Operator overloading methods to support Rect * float and float * Rect
    def __mul__(self, factor: float) -> "Rectangle":
        """Scale the rectangle by a given factor using the * operator."""
        return self.scale(factor)

    def __rmul__(self, factor: float) -> "Rectangle":
        """Scale the rectangle by a given factor using the * operator."""
        return self.scale(factor)

    def __eq__(self, other: object) -> bool:
        """Check if two rectangles are equal."""
        if not isinstance(other, Rectangle):
            return NotImplemented
        return self.width == other.width and self.height == other.height

    def __repr__(self) -> str:
        """Return a string representation of the rectangle."""
        return f"Rectangle(width={self.width}, height={self.height})"


def main() -> None:
    """Application entry point."""
    r = Rectangle(2, 3)
    print(f"Rectangle: {r * 2}")
    print(f"Rectangle: {2 * r}")


if __name__ == "__main__":
    main()
