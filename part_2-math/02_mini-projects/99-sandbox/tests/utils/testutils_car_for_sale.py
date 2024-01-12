"""Test utilities for CarForSale class"""
import string
from datetime import datetime, timedelta
from math import floor, isclose
from random import choice, uniform

from car_for_sale import CarForSale
from tests.utils.testutils import TestUtils


class CarForSaleTestUtils(TestUtils):
    """Test utilities for the CarForSale class"""

    @classmethod
    def is_approx_equal(cls, u: CarForSale, v: CarForSale) -> bool:
        def is_datetime_approx_equal(t1, t2):
            current_time = datetime.now()
            return isclose(
                floor((current_time - t1).total_seconds()),
                floor((current_time - t2).total_seconds()),
            )

        return (
            u.__class__ == v.__class__
            and isclose(u.model_year, v.model_year)
            and isclose(u.mileage, v.mileage)
            and isclose(u.price, v.price)
            and is_datetime_approx_equal(u.posted_datetime, v.posted_datetime)
        )

    @classmethod
    def random_vector(cls, *_) -> CarForSale:
        def get_random_datetime():
            return CarForSale.reference_date - timedelta(days=uniform(0, 10))

        random_model_year = floor(
            TestUtils.random_scalar(1900, datetime.now().year)
        )
        random_mileage = floor(TestUtils.random_scalar(0, 1e6))
        random_price = TestUtils.random_scalar(1e3, 500e3)
        random_posted_datetime = get_random_datetime()
        random_model = "".join(choice(string.ascii_letters) for _ in range(10))
        random_source = "".join(choice(string.ascii_letters) for _ in range(20))
        random_location = "".join(
            choice(string.ascii_letters) for _ in range(10)
        )
        random_description = "".join(
            choice(string.ascii_letters) for _ in range(10)
        )
        return CarForSale(
            random_model_year,
            random_mileage,
            random_price,
            random_posted_datetime,
            random_model,
            random_source,
            random_location,
            random_description,
        )
