"""
Shakedown for the plthlp package.
"""

from plthlp.helperslib import plot_function

def volume(t):
    """
    Volume over time: $ V(t) = \\frac{(t - 4)^3}{64} + 3.3 $
    """
    return (t - 4) ** 3 / 64 + 3.3


if __name__ == "__main__":
    plot_function(
        volume,
        tmin=0,
        tmax=10,
        tlabel="time (hr)",
        xlabel="volume (bbl)",
        title=volume.__doc__,
        grid=True,
        axes=True,
    )
