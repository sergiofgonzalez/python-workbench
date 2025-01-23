"""Illustrate how to use the profiler with a simple example."""

import sys

from profiler import create_profiler


def get_all_factors(num: int) -> list[int]:
    """Return all factors of the number given."""
    profiler = create_profiler(f"get_all_factors({num})")
    profiler.start()
    factors = []
    for factor in range(2, num + 1):
        while num % factor == 0:
            factors.append(factor)
            num = num / factor
    profiler.end()
    return factors


def main() -> None:
    """Application entry point."""
    if len(sys.argv) != 2:  # noqa: PLR2004
        print("An integer argument is required")
        sys.exit(1)
    else:
        try:
            num = int(sys.argv[1])
        except (TypeError, ValueError):
            print("An integer argument is required")
            sys.exit(1)
        factors = get_all_factors(num)
        print(f"Factors of {num}: {", ".join(str(factor) for factor in factors)}")


if __name__ == "__main__":
    main()
