"""Library supporting currency exchange rates."""

from currex.rate_hub import get_rate_hub

MAX = 0


def get_daily_rates(currency, num_days=MAX):
    rate_hub = get_rate_hub(currency)
    rates = rate_hub.get_rates(30 if num_days == MAX else num_days)
    return rates
