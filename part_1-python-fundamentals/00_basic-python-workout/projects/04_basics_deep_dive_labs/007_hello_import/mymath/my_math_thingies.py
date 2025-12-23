"""My math thingies module: where we define functions and constants related to math."""

_version = "0.1.0"

pi = 3.14159


def area(radius: float) -> float:
    """Calculate the area of a circle given its radius."""
    return pi * radius * radius
