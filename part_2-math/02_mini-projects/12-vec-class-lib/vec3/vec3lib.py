"""A class for 3D vectors"""
from vec import Vector


class Vec3(Vector):
    """A class for 3D vectors"""

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def zero(cls):
        return Vec3(0, 0, 0)

    def add(self, other):
        if not isinstance(other, Vec3):
            raise TypeError("Incompatible vectors")
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def scale(self, scalar):
        return Vec3(scalar * self.x, scalar * self.y, scalar * self.z)

    # def __mul__(self, scalar_or_natrix: Matrix_5_by_3):
    #     """Vec3 instances on the left"""
    #     if isinstance(scalar_or_natrix, Matrix_5_by_3):
    #         m = scalar_or_natrix
    #         return tuple(
    #             row[0] * self.x + row[1] * self.y + row[2] * self.z
    #             for row in m.matrix
    #         )
    #     else:
    #         return super().__rmul__(scalar_or_natrix)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __str__(self):
        """User friendly representation for users of the code"""
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return f"Vec3({self.x}, {self.y}, {self.z})"
