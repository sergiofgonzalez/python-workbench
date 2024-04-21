"""
__init__.py for the lines package that provides helper functions for
different line equations.

The names are awful 😟
"""

from lines.linelib import (
    canonical_line_coefficients,
    canonical_line_coefficients_point_vector,
    canonical_line_latex,
    fn_parametric_line,
    fn_std_form_line,
    fn_secant_line,
)

__all__ = [
    "canonical_line_coefficients",
    "canonical_line_coefficients_point_vector",
    "canonical_line_latex",
    "fn_parametric_line",
    "fn_std_form_line",
    "fn_secant_line",
]
