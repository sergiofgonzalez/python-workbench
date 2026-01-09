"""Illustrates the basics of shelve module."""

import shelve
from pathlib import Path

base_path = Path("data", "out_data", "tmp")


def main() -> None:
    """Application entry point."""
    shelve_file = base_path / "phone_book.shelve"

    with shelve.open(shelve_file) as phone_book:  # noqa: S301
        phone_book["Pugh"] = ("Florence", "555-1234", "123 Main St")
        phone_book["Isaacs"] = ("Jason", "555-5678", "456 Oak Ave")

    print(f"Wrote phone book data to {shelve_file}")

    # Now let's read back the shelved data
    with shelve.open(shelve_file) as phone_book:  # noqa: S301
        print(phone_book["Pugh"])
        print("=" * 40)
        # it behaves like a dictionary
        for last_name in phone_book:
            print(f"{last_name}: {phone_book[last_name]}")
        print("=" * 40)

        if "Isaacs" in phone_book:
            print(f"Found entry for Isaacs: {phone_book['Isaacs']}")
        print("=" * 40)

        for key, value in phone_book.items():
            print(f"{key}: {value}")
        print("=" * 40)

        del phone_book["Pugh"]
        print("Deleted entry for Pugh.")
        print(f"Remaining entries: {list(phone_book.keys())}")


if __name__ == "__main__":
    main()
