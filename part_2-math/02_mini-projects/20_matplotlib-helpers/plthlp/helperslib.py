"""
Matplotlib helper functions
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_function(
    fn,
    tmin,
    tmax,
    tlabel=None,
    xlabel=None,
    axes=False,
    grid=False,
    title=None,
    **kwargs
):
    """
    Plot a function of one variable x over t using matplotlib.
    """
    ts = np.linspace(tmin, tmax, 1000)
    if tlabel:
        plt.xlabel(tlabel)
    if xlabel:
        plt.ylabel(xlabel)

    total_t = tmax - tmin
    plt.xlim(tmin, tmax + total_t / 10)
    if grid:
        plt.grid(True)
    xs = [fn(t) for t in ts ]
    plt.plot(ts, xs, **kwargs)
    if axes:
        total_t = tmax - tmin
        plt.plot(
            [tmin - total_t / 10, tmax + total_t / 10], [0, 0], c="k", lw=1
        )
        plt.xlim(tmin - total_t / 10, tmax + total_t / 10)
        xmin, xmax = plt.ylim()
        plt.plot([0, 0], [xmin, xmax], c="k", lw=1)
        plt.ylim(xmin, xmax)

    if title:
        plt.title(title)

    plt.show()
