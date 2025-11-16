"""Practical examples of container type hints."""

from collections.abc import Sequence
from statistics import mean, stdev


def generate_stats(samples: list[float] | tuple[float, ...]) -> tuple[float, float]:
    """Generate basic statistics from a list or tuple of floats."""
    avg = mean(samples)
    stddev = stdev(samples)
    return avg, stddev


def generate_stats_v2(samples: Sequence[float]) -> dict[str, float]:
    """Generate basic statistics from a sequence of floats."""
    avg = mean(samples)
    stddev = stdev(samples)
    return {"mean": avg, "stddev": stddev}


def main() -> None:
    """Application entry point."""
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = generate_stats(data)
    print(f"Mean: {stats[0]}, Standard Deviation: {stats[1]}")

    # using a tuple instead
    tuple_data = (1, 2, 3, 4, 5)
    stats = generate_stats(tuple_data)
    print(f"Mean: {stats[0]}, Standard Deviation: {stats[1]}")

    stats = generate_stats_v2(data)
    print(f"Mean: {stats['mean']}, Standard Deviation: {stats['stddev']}")

    # using tuple data
    stats = generate_stats_v2(tuple_data)
    print(f"Mean: {stats['mean']}, Standard Deviation: {stats['stddev']}")


if __name__ == "__main__":
    main()
