"""A generic base class for vectors of any dimension"""


from abc import ABC, abstractmethod


class Vector(ABC):
    """Abstract class for vectors"""

    @classmethod
    @abstractmethod
    def zero(cls):
        ...

    @abstractmethod
    def scale(self, scalar):
        ...

    @abstractmethod
    def add(self, other):
        ...

    def subtract(self, other):
        return self.add(-1 * other)

    def __mul__(self, scalar):
        return self.scale(scalar)

    def __rmul__(self, scalar):
        return self.scale(scalar)

    def __add__(self, other):
        return self.add(other)

    def __sub__(self, other):
        return self.subtract(other)

    def __neg__(self):
        return self.scale(-1)

    def __truediv__(self, scalar):
        return self.scale(1.0 / scalar)
