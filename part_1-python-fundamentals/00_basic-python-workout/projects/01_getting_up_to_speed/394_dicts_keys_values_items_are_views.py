"""Illustrates dictionary views: keys, values, and items."""


def main() -> None:
    """Application entry point."""
    eng_to_french = {"red": "rouge", "green": "vert", "blue": "bleu"}

    # Get views of keys, values, and items
    keys_view = eng_to_french.keys()
    values_view = eng_to_french.values()
    items_view = eng_to_french.items()
    print(f"Keys view: {keys_view}")
    print(f"Values view: {values_view}")
    print(f"Items view: {items_view}")
    print("=" * 40)

    # Create a list from the keys view
    keys_list = list(keys_view)
    print(f"Keys list: {keys_list}")
    print("=" * 40)

    # We delete an entry and see what happens to the views and list
    del eng_to_french["red"]
    print("Deleted the entry for 'red'.")
    print(f"Keys view after deletion: {keys_view}")
    print(f"Values view after deletion: {values_view}")
    print(f"Items view after deletion: {items_view}")
    print(f"Keys list after deletion (should be unchanged): {keys_list}")
    print("=" * 40)

    assert "red" not in keys_view
    assert "rouge" not in values_view
    assert ("red", "rouge") not in items_view
    assert keys_list == ["red", "green", "blue"]


if __name__ == "__main__":
    main()
