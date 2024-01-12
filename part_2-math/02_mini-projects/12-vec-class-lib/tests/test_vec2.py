"""Unit tests for the Vec2 class"""
import unittest

from tests.utils.testutils_vec2 import Vec2TestUtils
from vec2 import Vec2


class TestVec2(unittest.TestCase):
    """
    Vec2 test class
    """

    def test_is_vector_space(self):
        """
        Validates that Vec2 is a vector space by checking that vector space
        rules work for 1000 random vectors and scalars.
        """
        for _ in range(1000):
            a, b = (
                Vec2TestUtils.random_scalar(),
                Vec2TestUtils.random_scalar(),
            )
            u, v, w = (
                Vec2TestUtils.random_vector(),
                Vec2TestUtils.random_vector(),
                Vec2TestUtils.random_vector(),
            )
            Vec2TestUtils().check_vector_space(a, b, u, v, w)

    def test_division(self):
        """
        Validates that you can divide a Vec2 by a scalar
        """
        u = Vec2TestUtils.random_vector()
        s = Vec2TestUtils.random_scalar()
        got = u / s
        expected = Vec2(u.x / s, u.y / s)
        self.assertTrue(Vec2TestUtils.is_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
