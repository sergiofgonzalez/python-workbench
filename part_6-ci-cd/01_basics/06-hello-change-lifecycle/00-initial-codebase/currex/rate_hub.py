"""Rate hub module."""

from abc import ABC, abstractmethod
from random import uniform

MAX_COUNT = 100


class RateHub(ABC):
    @abstractmethod
    def get_rates(self, num_days):
        pass


class EURRateHub(RateHub):
    """A rate hub for EUR currency used to get the daily rates for € in $"""

    def __init__(self):
        self.rates_min = 1.0
        self.rates_max = 1.2

    def get_rates(self, num_days):
        if num_days == 0:
            count = MAX_COUNT
        else:
            count = num_days
        return [uniform(self.rates_min, self.rates_max) for _ in range(count)]


def get_rate_hub(currency):
    if currency == "EUR":
        return EURRateHub()
    else:
        raise NotImplementedError(f"Currency {currency} is not supported")
