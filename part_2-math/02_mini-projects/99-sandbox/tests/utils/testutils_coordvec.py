"""Test utilities for CoordinateVector class"""
from math import isclose

from coordvec import CoordinateVector
from tests.utils.testutils import TestUtils


class CoordVecTestUtils(TestUtils):
    """Test utilities for CoordinateVector class"""

    @staticmethod
    def concrete_coordvec_class(dimension: int) -> CoordinateVector:
        class CoordinateVectorConcrete(CoordinateVector):
            @classmethod
            def dimension(cls):
                return dimension

        return CoordinateVectorConcrete

    @classmethod
    def random_coords(cls, dimension: int) -> tuple[int]:
        return tuple(cls.random_scalar() for _ in range(dimension))

    @classmethod
    def is_approx_equal(cls, u: CoordinateVector, v: CoordinateVector) -> bool:
        if (
            not isinstance(u, CoordinateVector)
            or not isinstance(v, CoordinateVector)
            or len(u.coordinates) != len(v.coordinates)
        ):
            return False

        return all(
            [
                isclose(coord_u, coord_v)
                for coord_u, coord_v in zip(u.coordinates, v.coordinates)
            ]
        )

    @classmethod
    def random_vector(cls, dimension: int) -> CoordinateVector:
        coordvec_class = cls.concrete_coordvec_class(dimension)
        random_coords = cls.random_coords(dimension)
        return coordvec_class(*random_coords)
