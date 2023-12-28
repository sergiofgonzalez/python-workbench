"""Unit test that validates that Vec2 is a vector space"""
import unittest

from vec2 import Vec2
from vec3 import Vec3

from .testutils import TestUtils


class TestVec3IsSpaceVector(unittest.TestCase):
    """Compiles the tests that checks that Vec3 is a space vector"""

    def test_is_space_vector(self):
        """
        Tests that Vec3 is a vector space by validating the six rules of vector
        spaces
        """
        for _ in range(1000):
            a, b = TestUtils.random_scalar(), TestUtils.random_scalar()
            u, v, w = (
                TestUtils.random_vec3(),
                TestUtils.random_vec3(),
                TestUtils.random_vec3(),
            )
            TestUtils().check_vector_space_rules(
                TestUtils.is_vec3_approx_equal, a, b, u, v, w
            )

    def test_duck_typing_vec3_fails(self):
        """
        Tests that comparisons such as Vec2(1, 2) == Vec3(1, 2, 3) do return
        False
        """
        u = Vec3(1, 2, 3)
        v = Vec2(1, 2)
        w = TestUtils.concrete_coordvec_class(dimension=5)(1, 2, 3, 4, 5)
        self.assertNotEqual(u, v)
        self.assertNotEqual(u, w)

    def test_division_vec3(self):
        u = TestUtils.random_vec3()
        s = TestUtils.random_scalar()
        got = u / s
        expected = Vec3(u.x / s, u.y / s, u.z / s)
        self.assertTrue(TestUtils.is_vec3_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
