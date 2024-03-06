"""
Library with the functions that return the line equations
"""

from typing import Callable, Tuple


def fn_parametric_line(
    u: Tuple[int, float], w: Tuple[float, float]
) -> Callable[[float], Tuple[float, float]]:
    """
    Returns the parametric line equation from two points "r(t) = u + t (w - u)"
    """
    ux, uy = u
    wx, wy = w
    return lambda t: (ux + t * (wx - ux), uy + t * (wy - uy))


def canonical_line_coefficients(
    p1: Tuple[float, float], p2: Tuple[float, float]
) -> Tuple[float, float, float]:
    """
    Returns the canonical line equation coefficients from two points
    "ax + by = c"
    """
    x1, y1 = p1
    x2, y2 = p2
    a = y2 - y1
    b = x1 - x2
    c = x1 * y2 - x2 * y1
    return a, b, c


def canonical_line_latex(a, b, c: float) -> str:
    """
    Returns the canonical line equation in LaTeX format
    """

    def get_coefficient(coef: float, variable: str) -> str:
        if coef == 0:
            return ""
        elif coef == 1:
            return variable
        elif coef == -1:
            return f"-{variable}"
        else:
            return f"{coef}{variable}"

    a_str = get_coefficient(a, "x")
    b_str = get_coefficient(b, "y")
    return f"$ {a_str} + {b_str} = {c} $"


def fn_std_form_line(a, b, c: float) -> Callable[[float], float]:
    """
    Returns a function that returns the value of y for a given x so that it can
    be easily plotted with Matplotlib.

    The function requires the coefficients a, b, c of the canonical line
    equation ax + by = c
    """
    return lambda x: (c - a * x) / b


def canonical_line_coefficients_point_vector(
    p: Tuple[float, float], v: Tuple[float, float]
) -> Tuple[float, float, float]:
    """
    Returns the canonical line equation coefficients for a line that passes
    through a point p and is perpendicular to vector v  "ax + by = c"
    """
    x0, y0 = p
    a, b = v
    return a, b, a * x0 + b * y0
