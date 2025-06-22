"""Appending items to a list programmatically."""


def main() -> None:
    """Application entry point."""
    nums = []
    for i in range(100):
        nums.append(i)  # noqa: PERF402
    print(f"List of numbers: {nums}")

if __name__ == "__main__":
    main()
