"""Models for the Asteroids game"""

from math import pi
from random import randint, uniform

from vec2d.math import to_cartesian, translate


class PolygonModel:
    """
    Represents a 2D shape in the game of Asteroids. A shape is defined by its
    points, its current rotation_angle, and its position.

    """

    def __init__(self, points) -> None:
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0

    def transformed(self):
        """
        Returns the list of points resulting of applying the corresponding
        translation and rotation status of the polygon to the points that define
        the polygon shape.
        """
        return translate((self.x, self.y), self.points)


class Ship(PolygonModel):
    """
    Represents the spaceship in the game of Asteroids. The ship is initially
    pointing to the right.
    """

    def __init__(self) -> None:
        super().__init__([(0.5, 0), (-0.25, 0.25), (-0.25, -0.25)])


class Asteroid(PolygonModel):
    """
    Represents an asteroid in the game of Asteroids. It is defined by a closed
    polygon of 5 to 9 sides.
    """

    def __init__(self) -> None:
        num_sides = randint(5, 9)
        points = [
            to_cartesian((uniform(0.5, 1.0), 2 * pi * n / num_sides))
            for n in range(num_sides)
        ]
        super().__init__(points)
