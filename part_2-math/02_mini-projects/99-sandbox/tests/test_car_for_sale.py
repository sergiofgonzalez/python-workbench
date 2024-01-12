"""Unit tests for the Vec3 class"""
import unittest

from car_for_sale import CarForSale
from tests.utils.testutils_car_for_sale import CarForSaleTestUtils


class TestCarForSale(unittest.TestCase):
    """
    Vec3 test class
    """

    def test_is_vector_space(self):
        """
        Validates that Vec3 is a vector space by checking that vector space
        rules work for 1000 random vectors and scalars.
        """
        for _ in range(1000):
            a, b = (
                CarForSaleTestUtils.random_scalar(),
                CarForSaleTestUtils.random_scalar(),
            )
            u, v, w = (
                CarForSaleTestUtils.random_vector(),
                CarForSaleTestUtils.random_vector(),
                CarForSaleTestUtils.random_vector(),
            )
            CarForSaleTestUtils().check_vector_space(a, b, u, v, w)


if __name__ == "__main__":
    unittest.main()
