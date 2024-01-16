"""Test utilities for the Matrix_5_by_3 class that inherits from Matrix"""
from math import isclose

from matrix_5_by_3 import Matrix_5_by_3
from tests.utils.testutils import TestUtils
from vec import Vector


class Matrix_5_by_3TestUtils(TestUtils):  # pylint: disable=C0103:invalid-name
    """Test utilities for the Matrix_5_by_3 class that inherits from Matrix"""

    @classmethod
    def is_approx_equal(cls, u: Matrix_5_by_3, v: Matrix_5_by_3) -> bool:
        if u.__class__ != v.__class__:
            return False
        for row_u, row_v in zip(u.matrix, v.matrix):
            for elem_u, elem_v in zip(row_u, row_v):
                if not isclose(elem_u, elem_v):
                    return False
        return True

    @classmethod
    def random_vector(cls, *_) -> Vector:
        return Matrix_5_by_3(
            tuple(
                tuple(
                    cls.random_scalar() for _ in range(Matrix_5_by_3.columns())
                )
                for _ in range(Matrix_5_by_3.rows())
            )
        )
