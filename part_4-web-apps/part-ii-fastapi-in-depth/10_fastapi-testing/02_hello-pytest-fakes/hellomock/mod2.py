"""
Module2 exposes certain functions to illustrate how to do mocking in Pytest
"""

import os

if os.getenv("UNIT_TEST"):
    from hellomock import fake_mod1 as mod1
else:
    from hellomock import mod1


def summer(x: int, y: int) -> str:
    return mod1.preamble() + f"{x + y}"
