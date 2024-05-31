"""Entry point for the currex application."""

import matplotlib.pyplot as plt

from currex.rates import get_daily_rates

if __name__ == "__main__":
    rates = get_daily_rates("EUR", 30)
    plt.plot(rates)
    plt.show()
