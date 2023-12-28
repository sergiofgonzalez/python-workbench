"""Unit test that validates that Vec2 is a vector space"""
import unittest

from vec2 import Vec2
from vec3 import Vec3

from .testutils import TestUtils


class TestCoordVecIsSpaceVector(unittest.TestCase):
    """Compiles the tests that checks that Vec3 is a space vector"""

    def test_is_space_vector(self):
        """
        Tests that CoordVec is a vector space by validating the six rules of
        vector for different dimensions
        """
        for test_dimension in range(4, 50):
            for _ in range(100):
                a, b = TestUtils.random_scalar(), TestUtils.random_scalar()
                u, v, w = (
                    TestUtils.concrete_coordvec_class(test_dimension)(
                        *TestUtils.random_coords(test_dimension)
                    ),
                    TestUtils.concrete_coordvec_class(test_dimension)(
                        *TestUtils.random_coords(test_dimension)
                    ),
                    TestUtils.concrete_coordvec_class(test_dimension)(
                        *TestUtils.random_coords(test_dimension)
                    ),
                )
                TestUtils().check_vector_space_rules(
                    TestUtils.is_vec_coords_approx_equal, a, b, u, v, w
                )

    def test_duck_typing_coordvec_fails(self):
        """
        Tests that comparisons such as Vec2(1, 2) == Vec3(1, 2, 3) do return
        False
        """
        u = TestUtils.concrete_coordvec_class(dimension=5)(1, 2, 3, 4, 5)
        v_1 = Vec2(1, 2)
        v_2 = Vec3(1, 2, 3)
        v_3 = TestUtils.concrete_coordvec_class(dimension=7)(
            1, 2, 3, 4, 5, 6, 7
        )
        self.assertNotEqual(u, v_1)
        self.assertNotEqual(u, v_2)
        self.assertNotEqual(u, v_3)

    def test_division(self):
        u = TestUtils.concrete_coordvec_class(dimension=5)(
            *TestUtils.random_coords(dimension=5)
        )
        s = TestUtils.random_scalar()
        got = u / s
        expected = TestUtils.concrete_coordvec_class(dimension=5)(
            *[u_coord / s for u_coord in u.coordinates]
        )
        self.assertTrue(TestUtils.is_vec_coords_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
