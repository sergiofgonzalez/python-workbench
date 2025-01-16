"""n1.py: module in the comp.numeric subpackage."""

from mathproj import version
from mathproj.comp import c1
from mathproj.comp.numeric.n2 import h


def g() -> None:
    """Print some things."""
    print(f"version is {version}")
    print(h())
