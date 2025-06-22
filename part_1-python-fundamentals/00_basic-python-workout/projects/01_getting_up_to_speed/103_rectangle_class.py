"""A basic Rectangle class."""


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
    r = Rectangle(3, 4)
    print(f"Rectangle: {r}")
    print(f"Area: {r.area()}")
    r_scaled = r.scale(2)
    print(f"Scaled Rectangle: {r_scaled}")
    print(f"Scaled Area: {r_scaled.area()}")
    r2 = Rectangle(3, 4)
    print(f"Are the rectangles equal? {r == r2}")
    print(f"Are the rectangles equal? {r == r_scaled}")


if __name__ == "__main__":
    main()
