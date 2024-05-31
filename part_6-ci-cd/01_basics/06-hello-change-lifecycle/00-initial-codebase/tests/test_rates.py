"""Test file for rates.py"""

import pytest

from currex.rates import get_daily_rates


def test_get_daily_rates_eur():
    rates = get_daily_rates("EUR", 10)
    assert len(rates) == 10


def test_get_daily_rates_not_supported():
    with pytest.raises(NotImplementedError):
        get_daily_rates("GBP")

