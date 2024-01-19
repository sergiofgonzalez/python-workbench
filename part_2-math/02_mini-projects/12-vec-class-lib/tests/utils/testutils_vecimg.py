"""Test utilities for the ImageVector class that inherits from Vector"""
from math import isclose
from random import randint

from tests.utils.testutils import TestUtils
from vec import Vector
from vecimg import ImageVector


class ImageVectorTestUtils(TestUtils):
    """Test utilities for the ImageVector class that inherits from Vector"""

    @staticmethod
    def random_scalar():
        return randint(0, 255)

    @classmethod
    def is_approx_equal(cls, u: ImageVector, v: ImageVector) -> bool:
        if u.__class__ != v.__class__:
            return False

        return  all(
                isclose(color_comp_u, color_comp_v)
                for pixel_u, pixel_v in zip(u.pixels, v.pixels)
                for color_comp_u, color_comp_v in zip(pixel_u, pixel_v)
         )

    @classmethod
    def random_vector(cls, *_) -> Vector:
        total_pixels = ImageVector.size[0] * ImageVector.size[1]
        return ImageVector(
            [
                (cls.random_scalar(), cls.random_scalar(), cls.random_scalar())
                for _ in range(total_pixels)
            ]
        )
