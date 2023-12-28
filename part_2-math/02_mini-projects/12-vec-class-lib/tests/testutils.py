"""Test utilities for the Vector class library"""
import unittest
from math import isclose
from random import uniform

from coordvec import CoordinateVector
from vec2 import Vec2
from vec3 import Vec3


class TestUtils(unittest.TestCase):
    """Utility methods"""

    @staticmethod
    def random_scalar(min_range=-10, max_range=10):
        return uniform(min_range, max_range)

    @staticmethod
    def random_coords(dimension, custom_random_coord_fn=None):
        if custom_random_coord_fn is None:
            custom_random_coord_fn = TestUtils.random_scalar

        return tuple(custom_random_coord_fn() for _ in range(dimension))

    @staticmethod
    def concrete_coordvec_class(dimension):
        class CoordinateVectorConcrete(CoordinateVector):
            @classmethod
            def dimension(cls):
                return dimension

        return CoordinateVectorConcrete

    @staticmethod
    def is_vec_coords_approx_equal(u, v):
        if (
            not isinstance(u, CoordinateVector)
            or not isinstance(v, CoordinateVector)
            or len(u.coordinates) != len(v.coordinates)
        ):
            return False

        return all(
            [
                isclose(coord_u, coord_v)
                for coord_u, coord_v in zip(u.coordinates, v.coordinates)
            ]
        )

    @staticmethod
    def random_vec2():
        return Vec2(TestUtils.random_scalar(), TestUtils.random_scalar())

    @staticmethod
    def random_vec3():
        return Vec3(
            TestUtils.random_scalar(),
            TestUtils.random_scalar(),
            TestUtils.random_scalar(),
        )

    @staticmethod
    def is_vec2_approx_equal(u, v):
        return (
            u.__class__ == v.__class__
            and isclose(u.x, v.x)
            and isclose(u.y, v.y)
        )

    @staticmethod
    def is_vec3_approx_equal(u, v):
        return (
            u.__class__ == v.__class__
            and isclose(u.x, v.x)
            and isclose(u.y, v.y)
            and isclose(u.z, v.z)
        )

    def check_vector_space_rules(self, eq_fn, a, b, u, v, w):
        # Required for vector spaces
        self.assertTrue(eq_fn(u + v, v + u))
        self.assertTrue(eq_fn(u + (v + w), (u + v) + w))
        self.assertTrue(eq_fn(a * (b * u), (a * b) * u))
        self.assertTrue(eq_fn(1 * u, u))
        self.assertTrue(eq_fn(a * u + b * u, (a + b) * u))
        self.assertTrue(eq_fn(a * (u + v), a * u + a * v))

        # Corollaries
        zero_v = u.__class__.zero()
        self.assertTrue(eq_fn(zero_v + u, u))
        self.assertTrue(eq_fn(0 * u, zero_v))
        self.assertTrue(eq_fn(-v + v, zero_v))
