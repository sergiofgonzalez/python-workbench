"""Unit tests for the ImageVector class which inherits from Vecotr"""
import unittest

from tests.utils.testutils_vecimg import ImageVectorTestUtils
from tests.utils.testutils import TestUtils


class ImageVectorTest(unittest.TestCase):
    """
    ImageVector test class
    """

    def test_is_vector_space(self):
        """
        Validates that ImageVector is a vector space by checking that vector
        space rules work for 1000 random vectors (images) and scalars.

        This is a long running test
        """
        for _ in range(10):
            a, b = (
                TestUtils.random_scalar(),
                TestUtils.random_scalar(),
            )
            u, v, w = (
                ImageVectorTestUtils.random_vector(),
                ImageVectorTestUtils.random_vector(),
                ImageVectorTestUtils.random_vector(),
            )
            ImageVectorTestUtils().check_vector_space(a, b, u, v, w)


if __name__ == "__main__":
    unittest.main()
