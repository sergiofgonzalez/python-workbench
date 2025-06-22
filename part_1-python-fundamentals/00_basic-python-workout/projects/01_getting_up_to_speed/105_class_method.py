"""Illustrate how to define class methods."""


class Rectangle:
    """A class representing a rectangle."""

    @classmethod
    def square(cls, side_length: float) -> "Rectangle":
        """Create a square rectangle with equal width and height."""
        if side_length <= 0:
            msg = "Side length must be positive."
            raise ValueError(msg)
        return cls(width=side_length, height=side_length)

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
    r = Rectangle.square(5)
    print(f"Square Rectangle: {r}")
    print(f"Area of square: {r.area()}")

    # You can invoke the class method from an instance as well
    print(f"Square Rectangle: {r.square(3)}")


if __name__ == "__main__":
    main()
