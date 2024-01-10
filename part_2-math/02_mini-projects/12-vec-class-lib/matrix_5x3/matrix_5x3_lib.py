"""A class representing 5x3 matrices as vectors"""
from vec import Vector


class Matrix5x3(Vector):
    """A class that represents a 5x3 matrix as a Vector"""

    rows = 5
    columns = 3

    def __init__(self, matrix):
        self.matrix = matrix

    @classmethod
    def zero(cls):
        return Matrix5x3(
            tuple(tuple(0 for _ in range(cls.columns)) for _ in range(cls.rows))
        )

    def add(self, other):
        if not isinstance(other, Matrix5x3):
            raise TypeError("Incompatible vectors")

        return Matrix5x3(
            tuple(
                tuple(a + b for a, b in zip(row1, row2))
                for row1, row2 in zip(self.matrix, other.matrix)
            )
        )

    def scale(self, scalar):
        return Matrix5x3(
            tuple(tuple(scalar * elem for elem in row) for row in self.matrix)
        )

    # Implementation with indices
    # def add(self, other):
    #     if not isinstance(other, Matrix5x3):
    #         raise TypeError("Incompatible vectors")

    #     return Matrix5x3(
    #         tuple(
    #             tuple(
    #                 self.matrix[i][j] + other.matrix[i][j]
    #                 for j in range(Matrix5x3.columns)
    #             )
    #             for i in range(Matrix5x3.rows)
    #         )
    #     )

    # Implementation with indices
    # def scale(self, scalar):
    #     return Matrix5x3(
    #         tuple(
    #             tuple(
    #                 scalar * self.matrix[i][j] for j in range(Matrix5x3.columns)
    #             )
    #             for i in range(Matrix5x3.rows)
    #         )
    #     )

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
        return f"Matrix5x3{repr(self.matrix)}"
