"""Test utilities for Vec0 class"""
from tests.utils.testutils import TestUtils
from vec0 import Vec0


class Vec0TestUtils(TestUtils):
    """Test utilities for the Vec0 class"""

    @classmethod
    def is_approx_equal(cls, u: Vec0, v: Vec0) -> bool:
        return u.__class__ == v.__class__

    @classmethod
    def random_vector(cls, *_) -> Vec0:
        return Vec0()
