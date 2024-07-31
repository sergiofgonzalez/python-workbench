"""Models for the Asteroids game"""

from math import pi, sqrt
from random import randint, uniform
from typing import Generator

import numpy as np
from vec2d.math import add, distance, rotate, to_cartesian, translate, scale


class PolygonModel:
    """
    Represents a 2D shape in the game of Asteroids. A shape is defined by its
    points, its current rotation_angle, and its position.

    """

    X_MIN = -10
    X_MAX = 10
    Y_MIN = -10
    Y_MAX = 10

    BOUNCE = True

    @staticmethod
    def standard_form(p1, p2) -> tuple[float, float, float]:
        """
        Returns a tuple (a, b, c) representing the coefficients of the
        linear equation in standard form ax + by = c representing the
        straight line passing through the given points p1, p2.
        """
        x1, y1 = p1
        x2, y2 = p2
        a = y2 - y1
        b = x1 - x2
        c = x1 * y2 - x2 * y1
        return a, b, c

    @staticmethod
    def intersection(u1, u2, v1, v2):
        a1, b1, c1 = PolygonModel.standard_form(u1, u2)
        a2, b2, c2 = PolygonModel.standard_form(v1, v2)
        m = np.array(((a1, b1), (a2, b2)))
        c = np.array((c1, c2))
        return np.linalg.solve(m, c)

    @staticmethod
    def do_segments_intersect(s1, s2):
        """
        Returns True if the segments defined by s1 and s2 intersect.
        s1 and s2 are a tuple of two elements, with each element being a point
        that defines the segment.
        """
        u1, u2 = s1
        v1, v2 = s2
        d1, d2 = distance(*s1), distance(*s2)
        try:
            x, y = PolygonModel.intersection(u1, u2, v1, v2)
            return (
                distance(u1, (x, y)) <= d1
                and distance(u2, (x, y)) <= d1
                and distance(v1, (x, y)) <= d2
                and distance(v2, (x, y)) <= d2
            )
        except np.linalg.LinAlgError:
            return False

    def __init__(self, points) -> None:
        self.points = points
        self.rotation_angle = 0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0

    def move(self, milliseconds, thrust_vector, gravity_source):
        tx, ty = thrust_vector
        gx, gy = gravitational_field(gravity_source, self.x, self.y)
        ax = tx + gx
        ay = ty + gy
        self.vx += ax * milliseconds / 1000
        self.vy += ay * milliseconds / 1000

        dx, dy = (
            self.vx * milliseconds / 1000.0,
            self.vy * milliseconds / 1000.0,
        )
        self.x, self.y = add((self.x, self.y), (dx, dy))

        if self.BOUNCE:
            if self.x < self.X_MIN or self.x > self.X_MAX:
                self.vx = -self.vx
            if self.y < self.Y_MIN or self.y > self.Y_MAX:
                self.vy = -self.vy
        else:
            if self.x < self.X_MIN:
                self.x += self.X_MAX - self.X_MIN
            if self.y < self.Y_MIN:
                self.y += self.Y_MAX - self.Y_MIN
            if self.x > self.X_MAX:
                self.x -= self.X_MAX - self.X_MIN
            if self.y > self.Y_MAX:
                self.y -= self.Y_MAX - self.Y_MIN

    def transformed(self):
        """
        Returns the list of points resulting of applying the corresponding
        translation and rotation status of the polygon to the points that define
        the polygon shape.
        """
        rotated_points = rotate(self.rotation_angle, self.points)
        return translate((self.x, self.y), rotated_points)

    def segments(
        self,
    ) -> Generator[tuple[tuple[float, float], tuple[float, float]], None, None]:
        """
        Returns the segments that define the Polygon
        """
        points = self.transformed()
        for i in range(len(points)):
            yield (points[i], points[(i + 1) % len(points)])

    def does_intersect(self, laser_beam_segment):
        """
        Returns True if the given segment intersects with any of the segments of
        the polygon, False otherwise
        """
        for segment in self.segments():
            if PolygonModel.do_segments_intersect(segment, laser_beam_segment):
                return True
        return False

    def does_collide(self, other_polygon):
        """
        Returns true if any of the segments of the polygon intersects with any
        of the segments of the other polygon given.
        """
        for segment in other_polygon.segments():
            if self.does_intersect(segment):
                return True
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
        laser_tip_polar = (max_dist, self.rotation_angle)
        return (ship_tip, to_cartesian(laser_tip_polar))


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
        self.vx = uniform(-1, 1)
        self.vy = uniform(-1, 1)


class BlackHole(PolygonModel):
    """
    Represents a black hole in the game of Asteroids. It is defined by a closed
    polygon of 20 vertices at equal distances (simulating a circle).
    The strength of the gravitational pull is determined by a single number
    gravity, which must be passed to the constructor
    """

    def __init__(self, gravity) -> None:
        vertices = [to_cartesian((0.5, 2 * pi * n / 20)) for n in range(20)]
        super().__init__(vertices)
        self.gravity = gravity

def gravitational_field(source, x, y):
    """
    Returns the gravitational field at the given point (x, y) due to the source.
    The source (black hole) creates a gravitational field that pulls objects
    towards it.
    To make the strength of the force field scale with the gravity, we multiply
    the field by the gravity of the source.
    """
    relative_position = (x - source.x, y - source.y)
    return scale(-source.gravity, relative_position)