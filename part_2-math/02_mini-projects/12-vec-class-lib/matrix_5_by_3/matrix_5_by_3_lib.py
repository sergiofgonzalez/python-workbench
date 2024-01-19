"""A class to represent Matrices of 5x3 inheriting from Matrix base class"""
from vec3 import Vec3
from vecmatrix import Matrix


class Matrix_5_by_3(Matrix):  # pylint: disable=C0103:invalid-name
    @classmethod
    def rows(cls):
        return 5

    @classmethod
    def columns(cls):
        return 3

    def __mul__(self, scalar_or_vector: float | Vec3):
        """Invoked when Matrix is on the left"""
        if isinstance(scalar_or_vector, Vec3):
            v = scalar_or_vector
            return tuple(
                row[0] * v.x + row[1] * v.y + row[2] * v.z
                for row in self.matrix
            )
        else:
            return super().__rmul__(scalar_or_vector)
