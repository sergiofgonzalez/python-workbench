"""Vector classes Test utilities Base class"""
import unittest
from abc import ABC, abstractmethod
from random import uniform
from typing import Optional

from vec import Vector


class TestUtils(ABC, unittest.TestCase):
    """Base class for unit testing utility methods"""

    @staticmethod
    def random_scalar(min_range=-10.0, max_range=10.0) -> float:
        """Returns a random scalar in the given range"""
        return uniform(min_range, max_range)

    @classmethod
    @abstractmethod
    def is_approx_equal(cls, u: Vector, v: Vector) -> bool:
        """
        Abstract method to be used while checking equality between vectors.
        Must be implemented in each and every concrete test utils class.
        """
        pass

    @classmethod
    @abstractmethod
    def random_vector(cls, dimension: Optional[int] = None) -> Vector:
        """
        Abstract method that returns a random vector for the corresponding class
        inheriting from Vector. In some situations, dimension must be provided
        (e.g., CoordVec), in other cases, it is an optional parameter.
        Must be implemented in each and every test utils class.
        """
        pass

    def check_vector_space(
        self, a: float, b: float, u: Vector, v: Vector, w: Vector
    ) -> None:
        """
        Perform all the vector space validations for the given vectors and
        scalars, using eq_fn as the function that checks for equality.
        """
        eq_fn = self.is_approx_equal
        zero_v = u.__class__.zero()

        # Required for vector spaces
        self.assertTrue(eq_fn(u + v, v + u))
        self.assertTrue(eq_fn(u + (v + w), (u + v) + w))
        self.assertTrue(eq_fn(a * (b * u), (a * b) * u))
        self.assertTrue(eq_fn(1 * u, u))
        self.assertTrue(eq_fn(a * u + b * u, (a + b) * u))
        self.assertTrue(eq_fn(a * (u + v), a * u + a * v))

        # Corollaries
        self.assertTrue(eq_fn(zero_v + u, u))
        self.assertTrue(eq_fn(0 * u, zero_v))
        self.assertTrue(eq_fn(-v + v, zero_v))
