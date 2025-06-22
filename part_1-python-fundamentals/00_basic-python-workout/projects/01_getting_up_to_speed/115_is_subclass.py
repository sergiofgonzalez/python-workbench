"""Checking if a class is a subclass of another class."""


class Vehicle:
    """Vehicle class."""


class Car(Vehicle):
    """Car class deriving from Vehicle."""


def main() -> None:
    """Application entry point."""
    c = Car()
    v = Vehicle()
    print(f"{isinstance(c, Vehicle)=}")  # returns True for subclasses
    print(f"{issubclass(Car, Vehicle)=}")
    print(f"{issubclass(Vehicle, Vehicle)=}")
    print(f"{issubclass(c.__class__, Vehicle)=}")
    print(f"{issubclass(c.__class__, v.__class__)=}")


if __name__ == "__main__":
    main()
