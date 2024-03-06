"""
Module2 exposes certain functions to illustrate how to do mocking in Pytest
"""


class MyClass:
    def __init__(self, preamble_provider):
        self.preamble_provider = preamble_provider

    def summer(self, x: int, y: int) -> str:
        return self.preamble_provider.preamble() + f"{x + y}"
