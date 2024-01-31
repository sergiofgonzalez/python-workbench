"""A class representing linear functions as 2D Vectors"""
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from typing_extensions import Self

from vec import Vector


class LinearFunction(Vector):
    """
    A class for that represents LinearFunctions as 2D vectors by storing the
    a, b coefficients of the f(x) = ax + b expression.
    """

    @staticmethod
    def plot(functions: Sequence[Self], xmin: float, xmax: float):
        xs = np.linspace(xmin, xmax, 100)
        _, ax = plt.subplots()
        ax.axhline(y=0, color="k")
        ax.axvline(x=0, color="k")
        fn_names = [
            fn._repr_latex_()
            for fn in functions  # pylint: disable=W0212:protected-access
        ]
        for f, fn_name in zip(functions, fn_names):
            ys = [f(x) for x in xs]
            plt.plot(xs, ys, label=fn_name)
        ax.legend()
        plt.show()

    def __init__(self, a, b: float) -> None:
        self.a = a
        self.b = b

    @classmethod
    def zero(cls):
        return LinearFunction(0, 0)

    def add(self, other):
        return LinearFunction(self.a + other.a, self.b + other.b)

    def scale(self, scalar):
        return LinearFunction(scalar * self.a, scalar * self.b)

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return f"LinearFunction({self.a}, {self.b})"

    def __str__(self):
        """User oriented representation of the function"""
        return f"{self.a}x + {self.b}"

    def _repr_latex_(self):
        """
        Convenience method to pretty-print Linear function instances in Jupyter
        notebooks using LaTeX
        """
        if self.a != 0 and self.b != 0:
            if self.a != 1:
                return f"$ {self.a} \\cdot x + {self.b} $"
            else:
                return f"$ x + {self.b} $"
        elif self.a == 0 and self.b != 0:
            return f"$ {self.b} $"
        elif self.a != 0 and self.b == 0:
            if self.a != 1:
                return f"$ {self.a} \\cdot x $"
            else:
                return "$ x $"
        else:
            return "$ 0 $"

    def __call__(self, x):
        return self.a * x + self.b
