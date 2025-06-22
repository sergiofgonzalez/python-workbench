"""Illustrate how to materialize ranges."""


def main() -> None:
    """Application entry point."""
    nums = range(5, 16)
    print(f"nums: {nums}")
    print(f"Materialized nums: {list(nums)}")


if __name__ == "__main__":
    main()
