"""OOP example involving shapes."""


class Shape:
    """Base class for shapes."""

    def __init__(self, x: float, y: float) -> None:
        """Initialize the shape with position (x, y)."""
        self.x = x
        self.y = y

    def move(self, delta_x: float, delta_y: float) -> None:
        """Move the shape by delta_x and delta_y."""
        self.x += delta_x
        self.y += delta_y

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the shape."""
        properties_str = ", ".join(f"{k}={v}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({properties_str})"


class Circle(Shape):
    """Class representing a circle shape."""

    pi = 3.14159
    all_circles: list["Circle"] | None = None

    def __init__(self, radius: float, x: float = 0, y: float = 0) -> None:
        """Initialize the circle with position (x, y) and radius."""
        super().__init__(x, y)
        self.radius = radius
        if Circle.all_circles is None:
            Circle.all_circles = []
        Circle.all_circles.append(self)

    @classmethod
    def total_area(cls) -> float:
        """Calculate the total area of all Circle instances."""
        if cls.all_circles is None:
            return 0.0
        return sum(Circle.circle_area(circle.radius) for circle in cls.all_circles)

    @staticmethod
    def circle_area(radius: float) -> float:
        """Calculate the area of a circle given its radius."""
        return Circle.pi * radius**2


def main() -> None:
    """Application entry point."""
    c1 = Circle(radius=1)
    print(f"{c1=}")
    print(f"{c1.radius=}")  # Access Circle-specific property
    print(f"{c1.x=}, {c1.y=}")  # Access Shape (superclass) properties
    print(f"{Circle.total_area()=}")  # Total area with one circle
    print("=" * 40)

    c2 = Circle(radius=2, x=3, y=4)
    print(f"{c2=}")
    c2.move(2, 2)  # Invoking superclass method
    print(f"After moving c2: {c2=}")
    print(f"{Circle.total_area()=}")  # Total area with two circles
    print("=" * 40)

    Circle.circle_area(c2.radius)  # Invoking Circle static method


if __name__ == "__main__":
    main()
