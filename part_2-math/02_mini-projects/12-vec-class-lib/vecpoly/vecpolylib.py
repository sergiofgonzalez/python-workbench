"""A class that represent polynomials as Vectors"""
from itertools import zip_longest

from vec import Vector


class Polynomial(Vector):
    """
    A class for Polynomials as vectors. To create an instance of this class
    you need to pass the coefficients of the polynomial starting from x^0, then
    x^1, x^2, etc.

    For example, 3*x^2 + 2*x - 5 is represented as Polynomial(-5, 2, 3)
    """

    def __init__(self, *coefficients: float) -> None:
        self.coefficients = coefficients

    @classmethod
    def zero(cls):
        Polynomial(0)

    def add(self, other):
        return Polynomial(
            *[
                c1 + c2
                for c1, c2 in zip_longest(
                    self.coefficients, other.coefficients, fillvalue=0
                )
            ]
        )

    def scale(self, scalar):
        return Polynomial(*[scalar * c for c in self.coefficients])

    def __str__(self):
        """User-oriented string representation"""
        monomials = []
        for power, coefficient in enumerate(self.coefficients):
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

        return " + ".join(monomials)

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return f"{self.__class__.__name__}{self.coefficients}"

    def _repr_latex_(self):
        """
        Convenience method to pretty-print Polynomial instances in Jupyter
        notebooks using LaTeX
        """
        monomials = []
        for power, coefficient in enumerate(self.coefficients):
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

        return f"$ {' + '.join(monomials)} $"

    def __call__(self, x):
        return sum(
            coefficient * x**power
            for power, coefficient in enumerate(self.coefficients)
        )
