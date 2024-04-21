"""Entry point for the application testing the functions in fnlib.py."""

import matplotlib.pyplot as plt
import numpy as np

from fns.fnlib import (
    approximate_integral,
    approximate_integral_fn,
    get_rate_of_change_fn,
    instantaneous_rate_of_change,
)


# We define a volume over time function and the corresponding flow rate function
def volume(t):
    """$ V(t) = \\frac{(t - 4)^3}{64} + 3.3 $"""
    return (t - 4) ** 3 / 64 + 3.3


def flow_rate(t):
    """$ flow(t) = \\frac{3 \\cdot (t - 4)^2}{64} $"""
    return 3 * (t - 4) ** 2 / 64


def plot_real_and_approximation_flow_rate():
    """Plots the real and approximation of the flow rate given the volume."""
    t_min = 0
    t_max = 10
    dt = 0.01

    ts = np.linspace(t_min, t_max)
    _, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel("Time (hr)")
    ax.set_ylabel("Flow Rate (bbl/hr)")
    ax.set_xlim(t_min - (t_max - t_min) * dt, t_max + (t_max - t_min) * dt)

    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")

    ax.plot(ts, [flow_rate(t) for t in ts], label="Real flow rate function")
    ax.plot(
        ts,
        [get_rate_of_change_fn(volume)(t) for t in ts],
        color="orange",
        label=f"Approximate flow rate function with 6 digits of precision",
    )

    ax.legend()
    plt.show()


def plot_real_and_approximation_volume():
    """Plots the real and approximation volume given the flow rate function."""
    t_min = 0
    t_max = 10
    dt = 0.01

    ts = np.linspace(t_min, t_max)
    _, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel("Time (hr)")
    ax.set_ylabel("Volume (bbl)")
    ax.set_xlim(t_min - (t_max - t_min) * dt, t_max + (t_max - t_min) * dt)

    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")

    ax.plot(ts, [volume(t) for t in ts], label="Real volume function")
    ax.plot(
        ts,
        [approximate_integral_fn(flow_rate, volume(0), dt)(t) for t in ts],
        color="orange",
        label=f"Approximate volume function for $\\Delta t = {dt}$",
    )

    ax.legend()
    plt.show()

if __name__ == "__main__":
    # Now we calculate the approximation given by the functions in our library
    # and compare them to the exact values

    print("Approximation of the flow rate given the volume at 3.75")
    approx = instantaneous_rate_of_change(volume, 3.75)
    real = flow_rate(3.75)

    print(
        f"Approximation: {approx} Real: {real} Difference: {abs(approx - real)}"
    )

    # Now we plot both and compare their graphs
    plot_real_and_approximation_volume()

    # Now we do the same with the integral
    print("Approximation of the volume given the flow rate at 3.75")
    approx = approximate_integral(flow_rate, volume(0), 0.01, 3.75)
    real = volume(3.75)
    print(
        f"Approximation: {approx} Real: {real} Difference: {abs(approx - real)}"
    )

    # Now we plot both and compare their graphs
    plot_real_and_approximation_flow_rate()