"""Illustrate the creation of class hierarchies and abstract classes."""

from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    """Abstract base class for all shapes."""

    @abstractmethod
    def area(self) -> float:
        """Calculate the area of the shape."""

    @abstractmethod
    def scale(self, factor: float) -> "Shape":
        """Return a new Rectangle scaled by a given factor."""

    def __eq__(self, other: object) -> bool:
        """Check if two shapes are equal."""
        if type(self) is not type(other):
            return False
        return all(
            other.__dict__.get(attr) == self.__dict__.get(attr)
            for attr in self.__dict__
        )

    def __mul__(self, factor: float) -> "Shape":
        """Scale the shape by a given factor using the * operator."""
        return self.scale(factor)

    def __rmul__(self, factor: float) -> "Shape":
        """Scale the shape by a given factor using the * operator."""
        return self.scale(factor)

    def __repr__(self) -> str:
        """Return a string representation of the shape."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"  # noqa: E501


class Rectangle(Shape):
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


class Square(Rectangle):
    """A class representing a square, derived from Rectangle."""

    def __init__(self, side_length: float) -> None:
        """Initialize the square with equal width and height."""
        super().__init__(width=side_length, height=side_length)

    def __repr__(self) -> str:
        """Return a string representation of the square."""
        return f"Square(side_length={self.width})"


class Circle(Shape):
    """A class representing a circle."""

    def __init__(self, radius: float) -> None:
        """Initialize the circle with a radius."""
        self.radius = radius

    def area(self) -> float:
        """Calculate the area of the circle."""
        return pi * (self.radius**2)

    def scale(self, factor: float) -> "Circle":
        """Return a new Circle scaled by a given factor."""
        if factor <= 0:
            msg = "Scale factor must be positive."
            raise ValueError(msg)
        return Circle(radius=self.radius * factor)


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
    print(f"Scaled Rectangle using * operator: {r * 2}")
    print(f"Scaled Rectangle using * operator: {2 * r}")

    print("\n--- Square ---")
    s = Square(5)
    print(f"Square: {s}")
    print(f"Area of square: {s.area()}")
    s_scaled = s.scale(2)
    print(f"Scaled Square: {s_scaled}")
    print(f"Scaled Area of square: {s_scaled.area()}")
    s2 = Square(5)
    print(f"Are the squares equal? {s == s2}")
    print(f"Are the square and rectangle equal? {s == r}")
    print(f"Scaled Square using * operator: {s * 2}")
    print(f"Scaled Square using * operator: {2 * s}")

    print("\n--- Circle ---")
    c = Circle(3)
    print(f"Circle: {c}")
    print(f"Area of circle: {c.area()}")
    c_scaled = c.scale(2)
    print(f"Scaled Circle: {c_scaled}")
    print(f"Scaled Area of circle: {c_scaled.area()}")
    c2 = Circle(3)
    print(f"Are the circles equal? {c == c2}")
    print(f"Scaled Circle using * operator: {c * 2}")
    print(f"Scaled Circle using * operator: {2 * c}")
    print(f"Is Rectangle equal to Square? {r == s}")
    print(f"Is Square equal to Circle? {s == c}")
    print(f"Is Circle equal to Circle? {c == c2}")
    print(f"Is Rectangle equal to Circle? {r == c}")


if __name__ == "__main__":
    main()
