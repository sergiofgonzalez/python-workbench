"""A Boat class with a complex initializer."""


class Boat:
    """Boat a class with a complex initializer."""

    def __init__(  # noqa: PLR0913
        self,
        has_motor: bool,  # noqa: FBT001
        motor_count: int,
        motor_brand: str,
        motor_model: str,
        has_sails: bool,  # noqa: FBT001
        sails_count: int,
        sails_material: str,
        sails_color: str,
        hull_color: str,
        has_cabin: bool,  # noqa: FBT001
    ) -> None:
        """Initialize a Boat instance."""
        self.has_motor = has_motor
        self.motor_count = motor_count
        self.motor_brand = motor_brand
        self.motor_model = motor_model
        self.has_sails = has_sails
        self.sails_count = sails_count
        self.sails_material = sails_material
        self.sails_color = sails_color
        self.hull_color = hull_color
        self.has_cabin = has_cabin

    def sail(self) -> None:
        """Announce itself."""
        print("Sailing the seas")
