"""Unit tests for the Function class"""
import unittest

from tests.utils.testutils_vecfunc import FunctionTestUtils


class TestFunction(unittest.TestCase):
    """
    Function test class
    """

    def test_is_vector_space(self):
        """
        Validates that Vec3 is a vector space by checking that vector space
        rules work for 1000 random vectors and scalars.

        This test takes about 2 seconds to complete.
        """
        for _ in range(1000):
            a, b = (
                FunctionTestUtils.random_scalar(),
                FunctionTestUtils.random_scalar(),
            )
            u, v, w = (
                FunctionTestUtils.random_vector(),
                FunctionTestUtils.random_vector(),
                FunctionTestUtils.random_vector(),
            )
            FunctionTestUtils().check_vector_space(a, b, u, v, w)


if __name__ == "__main__":
    unittest.main()
