"""Checking the type of a class."""


class Vehicle:
    """Vehicle class."""


class Car(Vehicle):
    """Car class deriving from Vehicle."""


def main() -> None:
    """Application entry point."""
    v = Vehicle()
    c = Car()
    print(f"{isinstance(v, Vehicle)=}")
    print(f"{isinstance(c, Car)=}")
    print(f"{isinstance(v, Car)=}")
    print(f"{isinstance(c, Vehicle)=}")  # returns True for subclasses


if __name__ == "__main__":
    main()
