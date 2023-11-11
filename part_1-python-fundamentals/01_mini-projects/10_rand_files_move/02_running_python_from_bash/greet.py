#!/usr/bin/env python

import sys


def get_hello(msg: str) -> str:
    """Returns a simple greeting"""
    return f"Hello to {msg}!"

if len(sys.argv) > 1:
    print(get_hello(" ".join(sys.argv[1:])))
else:
    print(get_hello("stranger"))
