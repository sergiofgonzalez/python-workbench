"""Unit test that validates that Vec2 is a vector space"""
import unittest

from vec0 import Vec0
from vec3 import Vec3

from .testutils import TestUtils


class TestVec0(unittest.TestCase):
    """Compiles the tests for Vec0 including checking it is a vector space"""

    def test_is_vector_space(self):
        """
        Tests that Vec0 is a vector space by validating the six rules of vector
        spaces
        """
        for _ in range(1000):
            a, b = TestUtils.random_scalar(), TestUtils.random_scalar()
            u, v, w = (
                TestUtils.random_vec0(),
                TestUtils.random_vec0(),
                TestUtils.random_vec0(),
            )
            TestUtils().check_vector_space_rules(
                TestUtils.is_vec0_approx_equal, a, b, u, v, w
            )

    def test_duck_typing_vec0_fails(self):
        """
        Tests that comparisons such as Vec0() == Vec3(1, 2, 3) do return
        False
        """
        u = Vec0()
        v = Vec3(1, 2, 3)
        w = TestUtils.concrete_coordvec_class(dimension=5)(1, 2, 3, 4, 5)
        self.assertNotEqual(u, v)
        self.assertNotEqual(u, w)

    def test_division_vec0(self):
        u = TestUtils.random_vec0()
        s = TestUtils.random_scalar()
        got = u / s
        expected = Vec0()
        self.assertTrue(TestUtils.is_vec0_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
