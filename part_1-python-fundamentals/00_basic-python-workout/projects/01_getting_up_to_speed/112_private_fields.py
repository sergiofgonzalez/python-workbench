"""Illustrate private and hidden attributes in Python classes."""


class Vehicle:
    """A class representing a vehicle."""

    def __init__(self, num_wheels: int, has_engine: bool) -> None:  # noqa: FBT001
        """Initialize the vehicle with number of wheels and engine status."""
        self._num_wheels = num_wheels
        self.__has_engine = has_engine  # Private attribute

    def __repr__(self) -> str:
        """Return a string representation of the vehicle."""
        return f"Vehicle(num_wheels={self._num_wheels}, has_engine={self.__has_engine})"


class Car(Vehicle):
    """A class representing a car, inheriting from Vehicle."""

    def __init__(self, num_wheels: int, brand: str) -> None:
        """Initialize the car with number of wheels, engine status, and brand."""
        super().__init__(
            num_wheels, True
        )  # Cars typically have an engine  # noqa: FBT003
        self.brand = brand
        self.__has_engine = (
            True  # Private attribute, shadowing Vehicle's private attribute
        )

    def __repr__(self) -> str:
        """Return a string representation of the car."""
        return f"Car(brand={self.brand}, num_wheels={self._num_wheels})"


def main() -> None:
    """Application entry point."""
    vehicle = Vehicle(4, True)  # noqa: FBT003
    print(vehicle)  # Output: Vehicle(num_wheels=4, has_engine=True)
    print(vehicle._num_wheels)  # Accessing protected attribute
    try:
        print(vehicle.__has_engine)  # Accessing private attribute (doesn't work)
    except AttributeError as e:
        print(e)  # Output: 'Vehicle' object has no attribute '__has_engine'

    print(vehicle.__dict__)  # Accessing all attributes

    car = Car(4, "Seat")
    print(car)  # Output: Car(brand=Toyota, num_wheels=4)
    # Accessing protected attribute
    print(car._num_wheels)  # Output: 4
    print(car.__dict__)

    # Attempting to access private attributes will raise an AttributeError
    try:
        print(car.__has_engine)
    except AttributeError as e:
        print(e)  # Output: 'Car' object has no attribute '__has_engine'


if __name__ == "__main__":
    main()
