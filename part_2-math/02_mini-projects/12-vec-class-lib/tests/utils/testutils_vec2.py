"""Test utilities for Vec2 class"""
from math import isclose

from tests.utils.testutils import TestUtils
from vec2 import Vec2


class Vec2TestUtils(TestUtils):
    """Test utilities for the Vec2 class"""

    @classmethod
    def is_approx_equal(cls, u: Vec2, v: Vec2) -> bool:
        return (
            u.__class__ == v.__class__
            and isclose(u.x, v.x)
            and isclose(u.y, v.y)
        )

    @classmethod
    def random_vector(cls, *_) -> Vec2:
        return Vec2(TestUtils.random_scalar(), TestUtils.random_scalar())
