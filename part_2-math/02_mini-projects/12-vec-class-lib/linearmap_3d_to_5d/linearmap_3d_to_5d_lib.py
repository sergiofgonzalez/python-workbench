"""A class representing Linear Map transformations from 3D to 5D as Vectors"""
from typing import Any

from coordvec import CoordinateVector
from vec import Vector


class LinearMap_3D_to_5D(Vector):  # pylint: disable=C0103:invalid-name
    """
    A class that represents Linear Map transformations from 3D to 5D as
    Vectors.
    The linear map is defined as a 5x3 matrix.
    """

    num_rows = 5
    num_columns = 3

    def __init__(self, matrix: tuple[tuple[float]]):
        if len(matrix) != self.num_rows or any(
            [len(matrix_row) != self.num_columns for matrix_row in matrix]
        ):
            raise TypeError(
                (
                    f"A tuple of {self.num_rows} rows "
                    f"by {self.num_columns} columns is required "
                    "to specify the linear map"
                )
            )
        self.matrix = matrix

    @classmethod
    def zero(cls):
        return cls(
            tuple(
                tuple(0 for _ in range(cls.num_columns))
                for _ in range(cls.num_rows)
            )
        )

    def add(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError("Incompatible vectors")

        return self.__class__(
            tuple(
                tuple(a + b for a, b in zip(row1, row2))
                for row1, row2 in zip(self.matrix, other.matrix)
            )
        )

    def scale(self, scalar):
        return self.__class__(
            tuple(tuple(scalar * elem for elem in row) for row in self.matrix)
        )

    def __call__(self, v: CoordinateVector) -> CoordinateVector:
        if v.dimension() != 3:
            return TypeError(
                "Expected 3D vector but got {v.dimension} dimensional vector"
            )

        return tuple(
            sum(
                tuple(
                    (elem_m * elem_v)
                    for elem_m, elem_v in zip(row, v.coordinates)
                )
            )
            for row in self.matrix
        )

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        for r1, r2 in zip(self.matrix, other.matrix):
            for e1, e2 in zip(r1, r2):
                if e1 != e2:
                    return False
        return True

    def __str__(self):
        """User-friendly representation for users of the code"""
        return str(self.matrix)

    def __repr__(self):
        """Dev-friendly representations for debugging purposes"""
        return f"{self.__class__.__name__}{repr(self.matrix)}"

    def _repr_latex_(self):
        """
        Convenience method to pretty-print Matrix instances in Jupyter
        notebooks using LaTeX
        """
        matrix_str = []
        for row in self.matrix:
            matrix_str.append(
                " & ".join([str(row_elem) for row_elem in row]) + "\\\\ \n"
            )

        matrix_str = "".join(matrix_str)
        return f"$ \\begin{{pmatrix}}\n{matrix_str}\\end{{pmatrix}} $"


class Vector3D(CoordinateVector):
    @classmethod
    def dimension(cls):
        return 3


class Vector5D(CoordinateVector):
    @classmethod
    def dimension(cls):
        return 5
