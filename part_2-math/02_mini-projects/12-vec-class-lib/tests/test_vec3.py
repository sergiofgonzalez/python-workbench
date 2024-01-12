"""Unit tests for the Vec3 class"""
import unittest

from tests.utils.testutils_vec3 import Vec3TestUtils
from vec3 import Vec3


class TestVec3(unittest.TestCase):
    """
    Vec3 test class
    """

    def test_is_vector_space(self):
        """
        Validates that Vec3 is a vector space by checking that vector space
        rules work for 1000 random vectors and scalars.
        """
        for _ in range(1000):
            a, b = (
                Vec3TestUtils.random_scalar(),
                Vec3TestUtils.random_scalar(),
            )
            u, v, w = (
                Vec3TestUtils.random_vector(),
                Vec3TestUtils.random_vector(),
                Vec3TestUtils.random_vector(),
            )
            Vec3TestUtils().check_vector_space(a, b, u, v, w)

    def test_division(self):
        """
        Validates that you can divide a Vec3 by a scalar
        """
        u = Vec3TestUtils.random_vector()
        s = Vec3TestUtils.random_scalar()
        got = u / s
        expected = Vec3(u.x / s, u.y / s, u.z / s)
        self.assertTrue(Vec3TestUtils.is_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
