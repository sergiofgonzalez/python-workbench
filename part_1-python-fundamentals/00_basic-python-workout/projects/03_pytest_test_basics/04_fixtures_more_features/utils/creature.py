"""A simple class representing a creature with basic attributes and behaviors."""


class Creature:
    """A class representing a creature with various attributes."""

    def __init__(
        self,
        name: str,
        description: str,
        country: str,
        area: str,
        aka: str,
    ) -> None:
        """Initialize a Creature instance with given attributes."""
        self.name = name
        self.description = description
        self.country = country
        self.area = area
        self.aka = aka
