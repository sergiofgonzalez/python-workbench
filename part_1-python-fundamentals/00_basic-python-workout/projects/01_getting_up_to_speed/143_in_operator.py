"""Illustrate the use of the `in` operator to check for membership."""


def main() -> None:
    """Application entry point."""
    print("=== lists ===")
    l1 = [1, 2, 3]
    print(f"{l1=}: {1 in l1=}")
    print(f"{l1=}: {5 in l1=}")  # noqa: PLR2004

    # dictionaries
    print("\n=== dictionaries ===")
    countries = {
        "fr": "France",
        "es": "Spain",
        "it": "Italy",
    }
    print(countries)
    print(f"{"es" in countries=}")
    print(f"{"gb" in countries=}")


if __name__ == "__main__":
    main()
