"""A base class representing matrices as vectors"""
from abc import abstractmethod

from vec import Vector


class Matrix(Vector):
    """A class that represents a matrix as a Vector"""

    def __init__(self, matrix: tuple[tuple[float]]):
        if len(matrix) != self.rows() or any(
            [len(matrix_row) != self.columns() for matrix_row in matrix]
        ):
            raise TypeError(
                (
                    f"A tuple of {self.rows()} rows "
                    f"by {self.columns()} columns is required"
                )
            )
        self.matrix = matrix

    @classmethod
    @abstractmethod
    def rows(cls):
        pass

    @classmethod
    @abstractmethod
    def columns(cls):
        pass

    @classmethod
    def zero(cls):
        return cls(
            tuple(
                tuple(0 for _ in range(cls.columns()))
                for _ in range(cls.rows())
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
