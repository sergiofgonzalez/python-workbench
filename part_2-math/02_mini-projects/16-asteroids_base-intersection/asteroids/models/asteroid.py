"""Models for the Asteroids game"""

from math import pi, sqrt
from random import randint, uniform

from vec2d.math import rotate, to_cartesian, to_polar, translate


class PolygonModel:
    """
    Represents a 2D shape in the game of Asteroids. A shape is defined by its
    points, its current rotation_angle, and its position.

    """

    X_MIN = -10
    X_MAX = 10
    Y_MIN = 10
    Y_MAX = 10

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
        rotated_points = rotate(self.rotation_angle, self.points)
        return translate((self.x, self.y), rotated_points)

    def does_intersect(self, segment):
        """
        Returns True if the given segment intersects with any of the segments of
        the polygon, False otherwise
        """
        return False


class Ship(PolygonModel):
    """
    Represents the spaceship in the game of Asteroids. The ship is initially
    pointing to the right.
    """

    def __init__(self) -> None:
        super().__init__([(0.5, 0), (-0.25, 0.25), (-0.25, -0.25)])

    def laser_segment(self):
        max_width = self.X_MAX - self.X_MIN
        max_height = self.Y_MAX - self.Y_MIN

        max_dist = sqrt(max_width**2 + max_height**2)
        ship_tip, *_ = self.transformed()
        _, ship_tip_polar_angle = to_polar(ship_tip)
        laser_tip = (max_dist, ship_tip_polar_angle)
        return (ship_tip, to_cartesian(laser_tip))


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
