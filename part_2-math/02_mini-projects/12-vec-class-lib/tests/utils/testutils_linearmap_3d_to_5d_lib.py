"""Test utilities for the LinearMap_3D_to_5D class that inherits from Vector"""
from math import isclose

from linearmap_3d_to_5d import LinearMap_3D_to_5D
from tests.utils.testutils import TestUtils
from vec import Vector


class LinearMap_3D_to_5DTestUtils(
    TestUtils
):  # pylint: disable=C0103:invalid-name
    """
    Test utilities for the LinearMap_3D_to_5D class that inherits from Vector
    """

    @classmethod
    def is_approx_equal(
        cls, u: LinearMap_3D_to_5D, v: LinearMap_3D_to_5D
    ) -> bool:
        if u.__class__ != v.__class__:
            return False
        for row_u, row_v in zip(u.matrix, v.matrix):
            for elem_u, elem_v in zip(row_u, row_v):
                if not isclose(elem_u, elem_v):
                    return False
        return True

    @classmethod
    def random_vector(cls, *_) -> Vector:
        return LinearMap_3D_to_5D(
            tuple(
                tuple(
                    cls.random_scalar()
                    for _ in range(LinearMap_3D_to_5D.num_columns)
                )
                for _ in range(LinearMap_3D_to_5D.num_rows)
            )
        )
