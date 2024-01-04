"""One-dimensional vectors"""
from vec import Vector


class Vec0(Vector):
    """A zero-dimensional vector"""

    def __init__(self):
        pass

    @classmethod
    def zero(cls):
        return Vec0()

    def scale(self, scalar):
        if not isinstance(scalar, (float, int)):
            raise TypeError("Scalar must be a number")
        return Vec0()

    def add(self, other):
        if not isinstance(other, Vec0):
            raise TypeError("Incompatible vectors")
        return Vec0()

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __str__(self):
        return "()"

    def __repr__(self):
        return "Vec0()"
