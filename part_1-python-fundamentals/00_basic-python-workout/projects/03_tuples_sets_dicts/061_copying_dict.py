"""Illustrate how to copy a dict."""


def main() -> None:
    """Application entry point."""
    my_dict = {
        "USA": "Washington, D.C.",
        "Canada": "Ottawa",
        "Spain": "Madrid",
        "France": "Paris",
    }

    my_dict_copy = my_dict.copy()  # Create a shallow copy of the dictionary
    print("Original dictionary:", my_dict)
    print("Copied dictionary:", my_dict_copy)
    my_dict_copy["Germany"] = "Berlin"  # Modify the copied dictionary
    print("After modifying copied dictionary:")
    print("Original dictionary:", my_dict)
    print("Copied dictionary:", my_dict_copy)
    my_dict.clear()  # Clear the original dictionary
    print("After clearing original dictionary:")
    print("Original dictionary:", my_dict)
    print("Copied dictionary:", my_dict_copy)


if __name__ == "__main__":
    main()
