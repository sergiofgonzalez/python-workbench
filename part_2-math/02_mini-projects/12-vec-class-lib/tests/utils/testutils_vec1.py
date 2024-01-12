"""Test utilities for Vec1 class"""
from math import isclose

from tests.utils.testutils import TestUtils
from vec1 import Vec1


class Vec1TestUtils(TestUtils):
    """Test utilities for the Vec1 class"""

    @classmethod
    def is_approx_equal(cls, u: Vec1, v: Vec1) -> bool:
        return (
            u.__class__ == v.__class__
            and isclose(u.x, v.x)
        )

    @classmethod
    def random_vector(cls, *_) -> Vec1:
        return Vec1(TestUtils.random_scalar())
