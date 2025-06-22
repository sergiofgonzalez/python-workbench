"""Illustrate the basics of zip() function."""

def main() -> None:
    """Application entry point."""
    nums = [1, 2, 3]
    letters = ["a", "b", "c"]
    zipped = zip(nums, letters, strict=True)
    print(f"Zipped: {zipped}")
    for t in zipped:
        print(f"Tuple: {t}")


if __name__ == "__main__":
    main()
