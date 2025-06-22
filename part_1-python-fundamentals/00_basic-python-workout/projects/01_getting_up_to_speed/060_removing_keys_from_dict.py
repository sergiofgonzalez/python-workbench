"""Removing keys from a dictionary in Python."""


def main() -> None:
    """Application entry point."""
    person = {
        "name": "Jason",
        "age": 57,
        "city": "New York",
        "job": "Actor",
    }

    del person["age"]  # Remove a key-value pair by key
    print(person)

    popped_value = person.pop("city")  # Remove a key-value pair by key and return the value
    print(f"popped value: {popped_value}")
    print(person)

    # Using popitem() removes the last inserted key-value pair
    last_item = person.popitem()
    print(f"popped_item: {last_item}")
    print(person)

    # Clear the dictionary
    person.clear()
    print("After clearing:", person)


if __name__ == "__main__":
    main()
