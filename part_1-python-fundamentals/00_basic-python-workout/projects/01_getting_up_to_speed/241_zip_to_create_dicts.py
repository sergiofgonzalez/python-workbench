"""Illustrate how to create dictionaries from two lists using zip."""


def main() -> None:
    """Application entry point."""
    ids = [101, 102, 103]
    titles = ["Laundry", "Grocery shopping", "Car service"]

    tasks_by_id = dict(zip(ids, titles, strict=True))
    assert tasks_by_id == {101: "Laundry", 102: "Grocery shopping", 103: "Car service"}
    print("=== PASSED ===")


if __name__ == "__main__":
    main()
