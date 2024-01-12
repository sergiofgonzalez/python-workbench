"""A class for having Python functions as Vectors"""
from typing import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from typing_extensions import Self

from vec import Vector


class Function(Vector):
    """A class for Functions as vectors"""

    @staticmethod
    def plot(
        functions: Sequence[Self],
        xmin: float,
        xmax: float,
        fn_names: Sequence[str],
    ):
        xs = np.linspace(xmin, xmax, 100)
        _, ax = plt.subplots()
        ax.axhline(y=0, color="k")
        ax.axvline(x=0, color="k")
        for f, fn_name in zip(functions, fn_names):
            ys = [f(x) for x in xs]
            plt.plot(xs, ys, label=fn_name)
        ax.legend()
        plt.show()

    def __init__(self, fn: Callable[[float], float]) -> None:
        self.function = fn

    @classmethod
    def zero(cls):
        def new_fn(x):
            return 0

        return Function(new_fn)

    def add(self, other):
        def new_fn(x):
            return self.function(x) + other.function(x)

        return Function(new_fn)

    def scale(self, scalar):
        def new_fn(x):
            return scalar * self.function(x)

        return Function(new_fn)

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return "Function()"

    def __call__(self, x):
        return self.function(x)
