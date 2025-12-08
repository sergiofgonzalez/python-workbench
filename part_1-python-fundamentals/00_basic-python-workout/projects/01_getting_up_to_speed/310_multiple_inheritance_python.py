"""A simple multiple inheritance practical example."""

from enum import Enum, auto


class Vehicle:
    """Represent a Vehicle."""

    def __init__(self, make: str, model: str, color: str) -> None:
        """Initialize a Vehicle instance."""
        self.make = make
        self.model = model
        self.color = color

    def start(self) -> None:
        """Start the vehicle."""
        print(f"{self!r} started.")

    def stop(self) -> None:
        """Stop the vehicle."""
        print(f"{self!r} stopped.")

    def __repr__(self) -> str:
        """Developer-friendly representation of a Vehicle."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Car(Vehicle):
    """Represent a Car."""

    def drive(self) -> None:
        """Drive the car."""
        print(f"Driving {self!r}")


class AircraftEngineType(Enum):
    """Enum for the different types of Aircraft engines."""

    PROPELLER_MOTOR = auto()
    JET_ENGINE = auto()
    MOTORLESS = auto()

    def __repr__(self) -> str:
        """Developer-friendly representation of the enum."""
        return self.name


class Aircraft(Vehicle):
    """Represent an aircraft."""

    def __init__(
        self, make: str, model: str, color: str, engine_type: AircraftEngineType
    ) -> None:
        """Initialize an aircraft instance."""
        super().__init__(make, model, color)
        self.engine_type = engine_type

    def fly(self) -> None:
        """Fly the aircraft."""
        print(f"Flying {self!r}")


class FlyingCar(Car, Aircraft):
    """Represent a flying car."""


def main() -> None:
    """Application entry point."""
    # Vehicle class shakedown
    v = Vehicle("Mercedes", "Class A", "Grey")
    v.start()
    v.stop()
    print("=" * 40)

    # Car class shakedown
    c = Car("Mercedes", "Class A", "Grey")
    c.start()
    c.drive()
    c.stop()
    print("=" * 40)

    # Aircraft class shakedown
    c = Aircraft("Cessna", "172", "White", AircraftEngineType.PROPELLER_MOTOR)
    c.start()
    c.fly()
    c.stop()
    print("=" * 40)

    # Flying car shakedown
    c = FlyingCar("Terrafugia", "Transition", "Red", AircraftEngineType.JET_ENGINE)
    c.start()
    c.drive()
    c.fly()
    c.stop()
    print("=" * 40)


if __name__ == "__main__":
    main()
