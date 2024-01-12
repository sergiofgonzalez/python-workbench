"""A class for having Python functions taking 2 arguments as Vectors"""
from typing import Callable, Sequence

import numpy as np
from typing_extensions import Self
from vec3d.graph import Points3D, draw3d

from vec import Vector


class Function2(Vector):
    """A class for Functions taking two arguments as vectors"""

    def __init__(self, fn: Callable[[float, float], float]) -> None:
        self.function = fn

    @classmethod
    def zero(cls):
        return Function2(lambda x, y: 0)

    def add(self, other):
        return Function2(
            lambda x, y: self.function(x, y) + other.function(x, y)
        )

    def scale(self, scalar):
        return Function2(lambda x, y: scalar * self.function(x, y))

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return "Function2()"

    def __call__(self, x, y):
        return self.function(x, y)

    def plot(
        self,
        *,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
    ):
        xs = np.linspace(xmin, xmax, num=25)
        ys = np.linspace(ymin, ymax, num=25)

        draw3d(Points3D(*[(x, y, self.function(x, y)) for x in xs for y in ys]))

