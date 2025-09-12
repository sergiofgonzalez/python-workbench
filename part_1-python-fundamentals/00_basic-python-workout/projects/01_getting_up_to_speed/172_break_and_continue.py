"""Sample use of break and continue."""


def main() -> None:
    """Application entry point."""
    lst = [1, 2, 3, 4, 5]
    for num in lst:
        if num % 3 == 0:
            print(f"Skipping {num} as it is divisible by 3")
            continue
        if num == 4:  # noqa: PLR2004
            print(f"Breaking the loop at {num}")
            break
        print(f"Processing {num}")


if __name__ == "__main__":
    main()
