"""Check if a set is a superset of another set."""


def main() -> None:
    """Application entry point."""
    set1 = {"Idris", "Jason", "Kenneth"}
    set2 = {"Jason"}

    # Check if set1 is a superset of set2
    if set1.issuperset(set2):
        print(f"{set1} is a superset of {set2}")
    else:
        print(f"{set1} is not a superset of {set2}")

    # using the > operator
    if set1 > set2:
        print(f"{set1} is a superset of {set2} using the > operator")
    else:
        print(f"{set1} is not a superset of {set2} using the > operator")


if __name__ == "__main__":
    main()
