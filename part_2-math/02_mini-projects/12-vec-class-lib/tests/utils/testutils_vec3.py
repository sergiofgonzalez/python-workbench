"""Test utilities for Vec3 class"""
from math import isclose

from tests.utils.testutils import TestUtils
from vec3 import Vec3


class Vec3TestUtils(TestUtils):
    """Test utilities for the Vec3 class"""

    @classmethod
    def is_approx_equal(cls, u: Vec3, v: Vec3) -> bool:
        return (
            u.__class__ == v.__class__
            and isclose(u.x, v.x)
            and isclose(u.y, v.y)
            and isclose(u.z, v.z)
        )

    @classmethod
    def random_vector(cls, *_) -> Vec3:
        return Vec3(
            TestUtils.random_scalar(),
            TestUtils.random_scalar(),
            TestUtils.random_scalar(),
        )
