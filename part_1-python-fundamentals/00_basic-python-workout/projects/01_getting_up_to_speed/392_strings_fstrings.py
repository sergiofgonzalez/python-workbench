"""Illustrates the use of f-strings."""

import math


def main() -> None:
    """Application entry point."""
    print("0         1         2")
    print("0---------0---------0")
    print(f"{math.pi:10.5f}")
    print(f"{math.pi:0>10.5f}")

    x = 3.21
    print(f"{x=}")

    x = 3.21
    print(f"{x=:10.2f}")

    w = "hello"
    s = f"The word is {w!r}"
    print(s)

if __name__ == "__main__":
    main()
