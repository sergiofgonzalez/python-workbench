"""Library of function concepts."""

import numpy as np


def average_rate_of_change(f, a, b):
    """Return the average rate of change of f(x) from a to b.

    Args:
        f (function): A function of one variable.
        a (float): The starting point.
        b (float): The ending point.

    Returns:
        float: The average rate of change of f(x) from a to b.
    """
    return (f(b) - f(a)) / (b - a)


def slope_of_secant_line(f, a, b):
    """Return the slope of the secant line through f(x) at a and b.

    Args:
        f (function): A function of one variable.
        a (float): The starting point.
        b (float): The ending point.

    Returns:
        float: The slope of the secant line through f(x) at a and b.
    """
    return average_rate_of_change(f, a, b)


def secant_line_fn(f, a, b):
    """Return the function of the secant line through f(x) at a and b.

    Args:
        f (function): A function of one variable.
        a (float): The starting point.
        b (float): The ending point.

    Returns:
        function: The function of the secant line through f(x) at a and b.
    """
    return lambda x: f(a) + (x - a) * (f(b) - f(a)) / (b - a)


def interval_rates_of_change(f, a, b, dx):
    """Return the rates of change of f(x) on the interval [a, b].

    Args:
        f (function): A function of one variable.
        a (float): The starting point.
        b (float): The ending point.
        dx (float): The step size.

    Returns:
        list: The rates of change of f(x) on the interval [a, b].
    """
    xs = np.arange(a, b, dx)
    return [average_rate_of_change(f, x, x + dx) for x in xs]


def instantaneous_rate_of_change(f, x, digits=6):
    """Return the instantaneous rate of change of f(x) at x.

    Args:
        f (function): A function of one variable.
        x (float): The point at which to calculate the rate of change.
        digits (int): The number of digits of precision.

    Returns:
        float: The instantaneous rate of change of f(x) at x.
    """
    tolerance = 10**-digits
    h = 1
    approx = average_rate_of_change(f, x - h, x + h)
    for _ in range(2 * digits):
        h /= 10
        new_approx = average_rate_of_change(f, x - h, x + h)
        if abs(new_approx - approx) < tolerance:
            return round(new_approx, digits)
        else:
            approx = new_approx
    raise Exception("Derivative did not converge after {2 * digits} iterations")


def get_rate_of_change_fn(f):
    """Return the rate of change function of f(x).

    Args:
        f (function): A function of one variable.

    Returns:
        function: The rate of change function of f(x).
    """
    return lambda x: instantaneous_rate_of_change(f, x)


def brief_antiderivative_change(q, x, dx):
    """Return the change in the antiderivative of q(x) on the interval [x, x + dx].

    Args:
        q (function): A function of one variable.
        x (float): The starting point.
        dx (float): The step size.

    Returns:
        float: The change in the antiderivative of q(x) on the interval [x, x + dx].
    """
    return q(x) * dx


def brief_integral_change(q, x, dx):
    """Return the change in the integral of q(x) on the interval [x, x + dx].

    Args:
        q (function): A function of one variable.
        x (float): The starting point.
        dx (float): The step size.

    Returns:
        float: The change in the integral of q(x) on the interval [x, x + dx].
    """
    return q(x) * dx


def antiderivative_change(q, x1, x2, dx):
    """Return the change in the antiderivative of q(x) on the interval [x1, x2].

    Args:
        q (function): A function of one variable.
        x1 (float): The starting point.
        x2 (float): The ending point.
        dx (float): The step size.

    Returns:
        float: The change in the antiderivative of q(x) on the interval [x1, x2].
    """
    return sum(
        [brief_antiderivative_change(q, x, dx) for x in np.arange(x1, x2, dx)]
    )


def integral_change(q, x1, x2, dx):
    """Return the change in the integral of q(x) on the interval [x1, x2].

    Args:
        q (function): A function of one variable.
        x1 (float): The starting point.
        x2 (float): The ending point.
        dx (float): The step size.

    Returns:
        float: The change in the integral of q(x) on the interval [x1, x2].
    """
    return antiderivative_change(q, x1, x2, dx)


def approximate_antiderivative(q, v0, dx, x):
    """Return the approximate antiderivative of q(x) at x.

    Args:
        q (function): A function of one variable.
        v0 (float): The value of the antiderivative for x = 0.
        dx (float): The step size.
        x (float): The point at which to calculate the antiderivative.

    Returns:
        float: The approximate antiderivative of q(x) at x.
    """
    return v0 + antiderivative_change(q, 0, x, dx)


def approximate_integral(q, v0, dx, x):
    """Return the approximate integral of q(x) at x.

    Args:
        q (function): A function of one variable.
        v0 (float): The value of the integral for x = 0.
        dx (float): The step size.
        x (float): The point at which to calculate the integral.

    Returns:
        float: The approximate integral of q(x) at x.
    """
    return approximate_antiderivative(q, v0, dx, x)

def approximate_antiderivative_fn(q, v0, dx):
    """Return the approximate antiderivative of q(x) at x.

    Args:
        q (function): A function of one variable.
        v0 (float): The value of the antiderivative for x = 0.
        dx (float): The step size.

    Returns:
        function: The approximate antiderivative of q(x) at x.
    """
    return lambda x: approximate_antiderivative(q, v0, dx, x)


def approximate_integral_fn(q, v0, dx):
    """Return the approximate integral of q(x) at x.

    Args:
        q (function): A function of one variable.
        v0 (float): The value of the integral for x = 0.
        dx (float): The step size.

    Returns:
        function: The approximate integral of q(x) at x.
    """
    return approximate_antiderivative_fn(q, v0, dx)

def get_antiderivative_fn(q, v0, digits=6):
    """Return the antiderivative function of q(x).

    Args:
        q (function): A function of one variable.
        v0 (float): The value of the antiderivative for x = 0.
        digits (int): The number of digits of precision.

    Returns:
        function: The antiderivative function of q(x).
    """

    def antiderivative_fn(t):
        tolerance = 10**-digits
        dt = 1
        approx = v0 + antiderivative_change(q, 0, t, dt)
        for _ in range(digits * 2):
            dt = dt / 10
            next_approx = v0 + antiderivative_change(q, 0, t, dt)
            if abs(next_approx - approx) < tolerance:
                return round(next_approx, digits)
            else:
                approx = next_approx
        raise Exception(
            f"Antiderivative did not converge in {digits * 2} iterations"
        )

    return antiderivative_fn

def get_integral_fn(q, v0, digits=6):
    """Return the integral function of q(x).

    Args:
        q (function): A function of one variable.
        v0 (float): The value of the integral for x = 0.
        digits (int): The number of digits of precision.

    Returns:
        function: The integral function of q(x).
    """
    return get_antiderivative_fn(q, v0, digits)