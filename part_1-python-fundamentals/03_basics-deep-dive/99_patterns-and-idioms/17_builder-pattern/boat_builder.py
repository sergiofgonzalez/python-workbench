"""Builder pattern for the Boat class."""

from boat import Boat


class BoatBuilder:
    """Implementation of the Builder pattern for creating Boat objects."""

    def __init__(self) -> None:
        """Initialize the BoatBuilder attributes with default values."""
        self.has_motor = False
        self.motor_count = None
        self.motor_brand = None
        self.motor_model = None
        self.has_sails = False
        self.sails_count = None
        self.sails_material = None
        self.sails_color = None
        self.hull_color = "white"
        self.has_cabin = False

    def with_motors(self, count: int, brand: str, model: str) -> "BoatBuilder":
        """Configure the motor related information."""
        self.has_motor = True
        self.motor_count = count
        self.motor_brand = brand
        self.motor_model = model
        return self

    def with_sails(self, count: int, material: str, color: str) -> "BoatBuilder":
        """Configure the sails related information."""
        self.has_sails = True
        self.sails_count = count
        self.sails_material = material
        self.sails_color = color
        return self

    def with_hull_color(self, color: str) -> "BoatBuilder":
        """Configure the hull related information."""
        self.hull_color = color
        return self

    def with_cabin(self) -> "BoatBuilder":
        """Configure the cabin related information."""
        self.has_cabin = True
        return self

    def build(self) -> Boat:
        """Initialize an instance of Boat using the builder design pattern."""
        return Boat(
            has_motor=self.has_motor,
            motor_count=self.motor_count,
            motor_brand=self.motor_brand,
            motor_model=self.motor_model,
            has_sails=self.has_sails,
            sails_count=self.sails_count,
            sails_material=self.sails_material,
            sails_color=self.sails_color,
            hull_color=self.hull_color,
            has_cabin=self.has_cabin,
        )
