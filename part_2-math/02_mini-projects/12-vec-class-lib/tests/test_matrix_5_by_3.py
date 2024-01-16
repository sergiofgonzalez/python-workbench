"""Unit tests for the Matrix_5_by_3 class which inherits from Matrix"""
import unittest

from tests.utils.testutils_matrix_5_by_3 import Matrix_5_by_3TestUtils


class Matrix_5_by_3Test(
    unittest.TestCase
):  # pylint: disable=C0103:invalid-name
    """
    Matrix_5_by_3 test class
    """

    def test_is_vector_space(self):
        """
        Validates that Matrix_5_by_3 is a vector space by checking that vector
        space rules work for 1000 random matrices and scalars.
        """
        for _ in range(1000):
            a, b = (
                Matrix_5_by_3TestUtils.random_scalar(),
                Matrix_5_by_3TestUtils.random_scalar(),
            )
            u, v, w = (
                Matrix_5_by_3TestUtils.random_vector(),
                Matrix_5_by_3TestUtils.random_vector(),
                Matrix_5_by_3TestUtils.random_vector(),
            )
            Matrix_5_by_3TestUtils().check_vector_space(a, b, u, v, w)


if __name__ == "__main__":
    unittest.main()
