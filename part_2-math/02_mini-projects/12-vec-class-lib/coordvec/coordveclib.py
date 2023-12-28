"""A generic class for vectors of any dimension"""
from abc import abstractmethod

from vec3d.math import add, scale

from vec import Vector


class CoordinateVector(Vector):
    """A generic class that represents a vector with numeric coordinates of any
    given dimension"""

    @classmethod
    @abstractmethod
    def dimension(cls):
        """Returns the dimension of the CoordinateVector.
        Must be implemented in the subclass."""
        pass

    @classmethod
    def zero(cls):
        return cls(*tuple(0 for _ in range(cls.dimension())))

    def __init__(self, *coordinates):
        self.coordinates = tuple(coord for coord in coordinates)

    def scale(self, scalar):
        # self.__class__ lets you return an instance of a concrete class from
        # the abstract superclass implementation
        return self.__class__(*scale(scalar, self.coordinates))

    def add(self, other):
        # self.__class__ lets you return an instance of a concrete class from
        # the abstract superclass implementation
        if not isinstance(other, CoordinateVector) or len(
            self.coordinates
        ) != len(other.coordinates):
            raise TypeError("Incompatible vectors")
        return self.__class__(*add(self.coordinates, other.coordinates))

    def __eq__(self, other):
        # For some reason self.__class__ == other.__class__ failed in the tests
        if not isinstance(other, CoordinateVector) or len(
            self.coordinates
        ) != len(other.coordinates):
            return False
        return all(
            [
                coord_u == coord_v
                for coord_u, coord_v in zip(self.coordinates, other.coordinates)
            ]
        )

    def __str__(self):
        "User friendly representation"
        return str(self.coordinates)

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return f"{self.__class__.__qualname__}{self.coordinates}"
