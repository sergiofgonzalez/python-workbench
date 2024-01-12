"""Unit tests for the Vec2 class"""
import unittest

from tests.utils.testutils_vec1 import Vec1TestUtils
from vec1 import Vec1


class TestVec1(unittest.TestCase):
    """
    Vec1 test class
    """

    def test_is_vector_space(self):
        """
        Validates that Vec1 is a vector space by checking that vector space
        rules work for 1000 random vectors and scalars.
        """
        for _ in range(1000):
            a, b = (
                Vec1TestUtils.random_scalar(),
                Vec1TestUtils.random_scalar(),
            )
            u, v, w = (
                Vec1TestUtils.random_vector(),
                Vec1TestUtils.random_vector(),
                Vec1TestUtils.random_vector(),
            )
            Vec1TestUtils().check_vector_space(a, b, u, v, w)

    def test_division(self):
        """
        Validates that you can divide a Vec2 by a scalar
        """
        u = Vec1TestUtils.random_vector()
        s = Vec1TestUtils.random_scalar()
        got = u / s
        expected = Vec1(u.x / s)
        self.assertTrue(Vec1TestUtils.is_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
