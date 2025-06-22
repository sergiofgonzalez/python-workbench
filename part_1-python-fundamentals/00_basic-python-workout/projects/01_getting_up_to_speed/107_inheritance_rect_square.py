"""Illustrate the basics of inheritance by creating a Square derived from Rectangle."""


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


class Square(Rectangle):
    """A class representing a square, derived from Rectangle."""

    def __init__(self, side_length: float) -> None:
        """Initialize the square with equal width and height."""
        super().__init__(width=side_length, height=side_length)

    def __repr__(self) -> str:
        """Return a string representation of the square."""
        return f"Square(side_length={self.width})"


def main() -> None:
    """Application entry point."""
    r = Rectangle(5, 5)
    print(f"Square Rectangle: {r}")
    print(f"Area of square rectangle: {r.area()}")

    s = Square(5)
    print(f"Square: {s}")
    print(f"Area of square: {s.area()}")

    # Demonstrating inheritance
    print(f"Is Square a Rectangle? {'Yes' if isinstance(s, Rectangle) else 'No'}")
    print(f"Is Rectangle a Square? {'Yes' if isinstance(r, Square) else 'No'}")


if __name__ == "__main__":
    main()
