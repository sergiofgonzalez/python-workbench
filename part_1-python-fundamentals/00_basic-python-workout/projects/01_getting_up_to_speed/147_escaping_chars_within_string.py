"""Illustrate how to escape characters within a string."""


def main() -> None:
    """Application entry point."""
    actor = "Jason Isaacs"
    print(f"{actor} is an actor.")
    print(f"\"{actor}\" is an actor.")  # noqa: Q003


if __name__ == "__main__":
    main()
