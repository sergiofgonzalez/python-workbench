"""Practicing negative indices when slicing."""


def main() -> None:
    """Application entry point."""
    revenues_by_month = [95, 100, 80, 93, 92, 110, 102, 88, 96, 98, 115, 120]

    # Extract the revenue in January
    assert revenues_by_month[0] == 95  # noqa: PLR2004

    # Calculate the revenues in Q2 (April, May, June)
    assert revenues_by_month[3:6] == [93, 92, 110]

    # Extract the revenue in November using negative indices
    assert revenues_by_month[-2] == 115  # noqa: PLR2004

    # Calculate the revenues in Q4 (October, November, December) using negative indices
    assert revenues_by_month[-3:] == [98, 115, 120]

    # Extract the revenues discarding the first and last months using negative indices
    assert revenues_by_month[1:-1] == [100, 80, 93, 92, 110, 102, 88, 96, 98, 115]

    print("=== PASSED ===")


if __name__ == "__main__":
    main()
