"""Unit tests for the Vec0 class"""
import unittest

from tests.utils.testutils_vec0 import Vec0TestUtils
from vec0 import Vec0


class TestVec0(unittest.TestCase):
    """
    Vec0 test class
    """

    def test_is_vector_space(self):
        """
        Validates that Vec0 is a vector space by checking that vector space
        rules work for 1000 random vectors and scalars.
        """
        for _ in range(1000):
            a, b = (
                Vec0TestUtils.random_scalar(),
                Vec0TestUtils.random_scalar(),
            )
            u, v, w = (
                Vec0TestUtils.random_vector(),
                Vec0TestUtils.random_vector(),
                Vec0TestUtils.random_vector(),
            )
            Vec0TestUtils().check_vector_space(a, b, u, v, w)

    def test_division(self):
        """
        Validates that you can divide a Vec2 by a scalar
        """
        u = Vec0TestUtils.random_vector()
        s = Vec0TestUtils.random_scalar()
        got = u / s
        expected = Vec0()
        self.assertTrue(Vec0TestUtils.is_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
