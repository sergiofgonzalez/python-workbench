"""
Entry point for the application, demonstrating the use of the lines module.
"""

import matplotlib.pyplot as plt
import numpy as np
from vec2d.graph import Colors, Points, Segment, draw

from lines.linelib import (
    canonical_line_coefficients,
    canonical_line_coefficients_point_vector,
    canonical_line_latex,
    fn_parametric_line,
    fn_std_form_line,
    fn_secant_line,
)


def plot_parametric_line_through_points(u, w, t_range=(-2, 2)):
    """
    Plots the parametric line "r(t) = u + t (w - u)" through the points u and w
    and the given t range using vec2d.graph backend
    """
    line = fn_parametric_line(u, w)
    t_min, t_max = t_range
    draw(
        Segment(line(t_min), line(t_max), color=Colors.BLUE),  # type: ignore
        Points(*[line(t) for t in range(t_min, t_max + 1)], color=Colors.BLACK),  # type: ignore
    )


def get_canonical_line_coefficients(p1, p2):
    """
    Returns the canonical line equation coefficients from two points
    "ax + by = c"
    """
    a, b, c = canonical_line_coefficients(p1, p2)
    print(f"The canonical line equation is {a}x + {b}y = {c}")
    return a, b, c


def plot_line(a, b, c, x_range=(-5, 5)):
    """
    Plots the line given the coefficients of the line in its canonical form
    ax + by = c in the given range using Matplotlib backend
    """
    x_min, x_max = x_range
    xs = np.linspace(x_min, x_max)
    ys = fn_std_form_line(a, b, c)(xs)
    plt.plot(xs, ys, label=canonical_line_latex(a, b, c))
    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")
    plt.legend()
    plt.grid()
    plt.show()


def get_canonical_line_coefficients_point_vector(p, v):
    """
    Returns the canonical line equation coefficients from a point and a vector
    "ax + by = c"
    """
    a, b, c = canonical_line_coefficients_point_vector(p, v)
    print(f"The canonical line equation is {a}x + {b}y = {c}")
    return a, b, c


def plot_secant_line():

    def f(x):
        """$ y = x^2 $"""
        return x ** 2

    x_min = -10
    x_max = 10
    xs = np.arange(x_min, x_max)

    fig, ax = plt.subplots()
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")

    ax.plot(xs, [f(x) for x in xs], label=f.__doc__)
    ax.scatter(-5, f(-5), color="black")

    ax.legend()

    secant_line = fn_secant_line(f, -5.01, -4.99)
    xs = np.arange(-9, 2)
    ax.plot(xs, [secant_line(x) for x in xs], label="Secant line at x = -5")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    # plot_parametric_line_through_points((2, 3), (4, 2))
    # plot_line(*get_canonical_line_coefficients((2, 3), (1, 5)))
    # plot_line(*get_canonical_line_coefficients_point_vector((3, 5), (3, 2)))
    plot_secant_line()
