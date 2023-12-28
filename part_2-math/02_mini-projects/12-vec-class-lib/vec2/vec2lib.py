"""A class for 2D vectors"""

from vec import Vector


class Vec2(Vector):
    """A class for 2D vectors"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def zero(cls):
        return Vec2(0, 0)

    def add(self, other):
        if not isinstance(other, Vec2):
            raise TypeError("Incompatible vectors")
        return Vec2(self.x + other.x, self.y + other.y)

    def scale(self, scalar):
        return Vec2(scalar * self.x, scalar * self.y)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.x == other.x
            and self.y == other.y
        )

    def __str__(self):
        """User friendly representation for users of the code"""
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return f"Vec2({self.x}, {self.y})"
