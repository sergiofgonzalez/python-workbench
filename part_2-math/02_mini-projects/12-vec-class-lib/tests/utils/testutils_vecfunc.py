"""Test utilities for Function class"""
from math import isclose
from random import uniform, randint

from tests.utils.testutils import TestUtils
from vecfunc import Function
from vecpoly import Polynomial


class FunctionTestUtils(TestUtils):
    """Test utilities for the Function class"""

    @classmethod
    def is_approx_equal(cls, u: Function, v: Function) -> bool:
        if u.__class__ != v.__class__:
            return False

        for _ in range(100):
            x = uniform(-10, 10)
            if not isclose(u(x), v(x)):
                return False

        return True

    @classmethod
    def random_vector(cls, *_) -> Function:
        degree = randint(0, 10)
        p = Polynomial(*[uniform(-10, 10) for _ in range(degree)])
        return Function(p)
