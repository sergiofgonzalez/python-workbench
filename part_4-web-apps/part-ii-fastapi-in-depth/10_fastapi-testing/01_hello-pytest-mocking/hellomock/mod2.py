"""
Module2 exposes certain functions to illustrate how to do mocking in Pytest
"""

import hellomock.mod1 as mod1


def summer(x: int, y: int) -> str:
    return mod1.preamble() + f"{x + y}"
