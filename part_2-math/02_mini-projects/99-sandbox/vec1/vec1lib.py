"""One-dimensional vectors"""
from vec import Vector


class Vec1(Vector):
    """A one-dimensional vector"""

    def __init__(self, x):
        self.x = x

    @classmethod
    def zero(cls):
        return Vec1(0)

    def scale(self, scalar):
        if not isinstance(scalar, (float, int)):
            raise TypeError("Scalar must be a number")
        return Vec1(self.x * scalar)

    def add(self, other):
        if not isinstance(other, Vec1):
            raise TypeError("Incompatible vectors")
        return Vec1(self.x + other.x)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x

    def __str__(self):
        return f"({self.x})"

    def __repr__(self):
        return f"Vec1({self.x})"
