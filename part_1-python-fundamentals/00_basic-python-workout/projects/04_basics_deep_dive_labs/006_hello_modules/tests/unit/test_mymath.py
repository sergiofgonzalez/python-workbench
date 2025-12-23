"""Unit tests for the mymath module."""

from math import isclose, pi

import mymath


def test_area() -> None:
    """Test the area function."""
    radius = 3.0
    expected_area = mymath.pi * radius * radius
    assert mymath.area(radius) == expected_area


def test_pi_value() -> None:
    """Test the value of pi."""
    assert isclose(mymath.pi, pi, rel_tol=1e-5)
