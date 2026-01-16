"""Illustrate how to use a property decorator with a Rectangle class."""


class Rectangle:
    """Class representing a rectangle shape."""

    def __init__(self, width: float, height: float) -> None:
        """Initialize the rectangle with width and height."""
        if width <= 0 or height <= 0:
            msg = "Width and height must be positive."
            raise ValueError(msg)
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        """Get the width of the rectangle."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set the width of the rectangle."""
        if value <= 0:
            msg = "Width must be positive."
            raise ValueError(msg)
        self._width = value

    @property
    def height(self) -> float:
        """Get the height of the rectangle."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Set the height of the rectangle."""
        if value <= 0:
            msg = "Height must be positive."
            raise ValueError(msg)
        self._height = value

    @property
    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self._width * self._height


def main() -> None:
    """Application entry point."""
    r = Rectangle(4, 5)
    print(f"Rectangle width: {r.width}")
    print(f"Rectangle height: {r.height}")
    print(f"Rectangle area: {r.area}")

    try:
        r.width = -10  # This should raise a ValueError
    except ValueError as e:
        print(f"Caught an error when setting width: {e}")


if __name__ == "__main__":
    main()
