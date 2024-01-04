"""Unit test that validates that Vec2 is a vector space"""
import unittest

from vec1 import Vec1
from vec3 import Vec3

from .testutils import TestUtils


class TestVec1IsSpaceVector(unittest.TestCase):
    """Compiles the tests for Vec1 including checking it is a vector space"""

    def test_is_vector_space(self):
        """
        Tests that Vec1 is a vector space by validating the six rules of vector
        spaces
        """
        for _ in range(1000):
            a, b = TestUtils.random_scalar(), TestUtils.random_scalar()
            u, v, w = (
                TestUtils.random_vec1(),
                TestUtils.random_vec1(),
                TestUtils.random_vec1(),
            )
            TestUtils().check_vector_space_rules(
                TestUtils.is_vec1_approx_equal, a, b, u, v, w
            )

    def test_duck_typing_vec1_fails(self):
        """
        Tests that comparisons such as Vec1(1) == Vec3(1, 2, 3) do return
        False
        """
        u = Vec1(1)
        v = Vec3(1, 2, 3)
        w = TestUtils.concrete_coordvec_class(dimension=5)(1, 2, 3, 4, 5)
        self.assertNotEqual(u, v)
        self.assertNotEqual(u, w)

    def test_division_vec2(self):
        u = TestUtils.random_vec1()
        s = TestUtils.random_scalar()
        got = u / s
        expected = Vec1(u.x / s)
        self.assertTrue(TestUtils.is_vec1_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
