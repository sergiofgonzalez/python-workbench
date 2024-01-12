"""Unit tests for the CoordVec class"""
import unittest

from tests.utils.testutils_coordvec import CoordVecTestUtils


class TestCoordVec(unittest.TestCase):
    """
    Tests that CoordVec is a vector space by validating the six rules of
    vector for different dimensions and a few other CoordinateVector related
    tests.
    """

    def test_is_vector_space(self):
        """
        Validates that CoordinateVector with dimensions 1 to 50 are vector
        spaces.
        This test takes about a second to run.
        """
        for test_dimension in range(1, 50):
            for _ in range(100):
                a, b = (
                    CoordVecTestUtils.random_scalar(),
                    CoordVecTestUtils.random_scalar(),
                )
                u, v, w = (
                    CoordVecTestUtils.random_vector(dimension=test_dimension),
                    CoordVecTestUtils.random_vector(dimension=test_dimension),
                    CoordVecTestUtils.random_vector(dimension=test_dimension),
                )
                CoordVecTestUtils().check_vector_space(a, b, u, v, w)

    def test_duck_typing_equality_for_coordvec(self):
        """
        Validates that duck typing fails for CoordinateVector of different
        dimensions.
        """
        u = CoordVecTestUtils.random_vector(dimension=2)
        v = CoordVecTestUtils.random_vector(dimension=3)
        self.assertNotEqual(u, v)

    def test_division(self):
        """
        Validates that you can divide a CoordinateVector by a scalar
        """
        u = CoordVecTestUtils.random_vector(dimension=5)
        s = CoordVecTestUtils.random_scalar()
        got = u / s
        expected = CoordVecTestUtils.concrete_coordvec_class(dimension=5)(
            *[u_coord / s for u_coord in u.coordinates]
        )
        self.assertTrue(CoordVecTestUtils.is_approx_equal(got, expected))


if __name__ == "__main__":
    unittest.main()
