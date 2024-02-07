"""A class that represents Quadratic functions (ax^2 + bx + c) as Vectors"""

from typing import Callable, Sequence

import matplotlib.pyplot as plt
import numpy as np
from typing_extensions import Self

from vec import Vector


class QuadraticFunction(Vector):
    """
    A class representing Quadratic functions f(x) = a x^2 + b x + c as vectors.
    """

    @staticmethod
    def plot(functions: Sequence[Self], xmin: float, xmax: float):
        xs = np.linspace(xmin, xmax, 100)
        _, ax = plt.subplots()
        ax.axhline(y=0, color="k")
        ax.axvline(x=0, color="k")
        fn_names = [
            fn._repr_latex_() for fn in functions  # pylint: disable=W0212
        ]
        for f, fn_name in zip(functions, fn_names):
            ys = [f(x) for x in xs]
            plt.plot(xs, ys, label=fn_name)
        ax.legend()
        plt.show()

    def __init__(self, a, b, c: float) -> None:
        self.a = a
        self.b = b
        self.c = c

    @classmethod
    def zero(cls):
        return QuadraticFunction(0, 0, 0)

    def add(self, other):
        return QuadraticFunction(
            self.a + other.a, self.b + other.b, self.c + other.c
        )

    def scale(self, scalar):
        return QuadraticFunction(
            scalar * self.a, scalar * self.b, scalar * self.c
        )

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        a, b, c = self.a, self.b, self.c
        return f"QuadraticFunction({a=}, {b=}, {c=})"

    def __str__(self):
        """User oriented representation"""
        monomials = []
        for power, coefficient in enumerate((self.c, self.b, self.a)):
            match power:
                case 0:
                    if coefficient != 0:
                        monomials.append(str(coefficient))
                case 1:
                    if coefficient == 1:
                        monomials.append("x")
                    elif coefficient == -1:
                        monomials.append("-x")
                    elif coefficient != 0:
                        monomials.append(f"{coefficient}x")
                case _:
                    if coefficient == 1:
                        monomials.append(f"x^{power}")
                    elif coefficient == -1:
                        monomials.append(f"-x^{power}")
                    elif coefficient != 0:
                        monomials.append(f"{coefficient}x^{power}")

        return " + ".join(reversed(monomials))

    def _repr_latex_(self):
        """
        Convenience method to pretty-print QuadraticFunction instances in
        Jupyter notebooks using LaTeX
        """
        monomials = []
        for power, coefficient in enumerate((self.c, self.b, self.a)):
            match power:
                case 0:
                    if coefficient != 0:
                        monomials.append(str(coefficient))
                case 1:
                    if coefficient == 1:
                        monomials.append("x")
                    elif coefficient == -1:
                        monomials.append("-x")
                    elif coefficient != 0:
                        monomials.append(f"{coefficient} \\cdot x")
                case _:
                    if coefficient == 1:
                        monomials.append(f"x^{{{power}}}")
                    elif coefficient == -1:
                        monomials.append(f"-x^{{{power}}}")
                    elif coefficient != 0:
                        monomials.append(f"{coefficient} \\cdot x^{{{power}}}")

        return f"$ {' + '.join(reversed(monomials))} $"

    def __call__(self, x):
        return self.a * x * x + self.b * x + self.c
