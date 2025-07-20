"""Illustrate the use of `len` and `in` in strings."""


def main() -> None:
    """Application entry point."""
    print(f"{len('Jason Isaacs')=}")
    print(f"{len('')=}")
    print(f"{len('😱')=}")
    print(f"{len('😱🛩️')=}")
    print(f"{len('🛩️')=}")

    print(f"{'Jason Isaacs' in 'Jason Isaacs'}")  # noqa: PLR0133
    print(f"{'Jason Isaacs' in 'Jason Isaacs is an actor'}")  # noqa: PLR0133
    print(f"{'son' in 'Jason Isaacs'}")  # noqa: PLR0133


if __name__ == "__main__":
    main()
