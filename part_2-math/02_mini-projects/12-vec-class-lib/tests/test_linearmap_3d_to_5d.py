"""Unit tests for the LinearMap_3D_to_5D class which inherits from Vector"""
import unittest

from mat import multiply_matrix_vector
from linearmap_3d_to_5d import Vector3D

from tests.utils.testutils_linearmap_3d_to_5d_lib import (
    LinearMap_3D_to_5DTestUtils,
)


class LinearMap_3D_to_5DTest(
    unittest.TestCase
):  # pylint: disable=C0103:invalid-name
    """
    LinearMap_3D_to_5D test class
    """

    def test_is_vector_space(self):
        """
        Validates that LinearMap_3D_to_5D is a vector space by checking that
        vector space rules work for 1000 underlying random matrices and scalars.
        """
        for _ in range(1000):
            a, b = (
                LinearMap_3D_to_5DTestUtils.random_scalar(),
                LinearMap_3D_to_5DTestUtils.random_scalar(),
            )
            u, v, w = (
                LinearMap_3D_to_5DTestUtils.random_vector(),
                LinearMap_3D_to_5DTestUtils.random_vector(),
                LinearMap_3D_to_5DTestUtils.random_vector(),
            )
            LinearMap_3D_to_5DTestUtils().check_vector_space(a, b, u, v, w)

    def test_linear_map_call_is_matrix_vector_mult(self):
        """
        Validates that invoking a linear map is the same as performing the
        corresponding matrix vector multiplication
        """
        for _ in range(1000):
            linear_map = LinearMap_3D_to_5DTestUtils.random_vector()
            v = (
                LinearMap_3D_to_5DTestUtils.random_scalar(),
                LinearMap_3D_to_5DTestUtils.random_scalar(),
                LinearMap_3D_to_5DTestUtils.random_scalar(),
            )

            self.assertEqual(
                linear_map(Vector3D(*v)),
                multiply_matrix_vector(linear_map.matrix, v),
            )


if __name__ == "__main__":
    unittest.main()
