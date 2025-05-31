"""Illustrate how to convert a dictionary to a list."""


def main() -> None:
    """Application entry point."""
    person = {
        "name": "Jason",
        "age": 57,
    }

    # Converting a dictionary to a list gives you a list of the keys
    person_list = list(person)
    print(person_list)

    # You can use items() to get the key-value pairs, but returns a dict_items object
    person_items = person.items()
    print(person_items)
    print(list(person_items))

    # You can use values() to get just the values, but returns a dict_values object
    person_values = person.values()
    print(person_values)
    print(list(person_values))

    # You can use keys() to get just the keys, but returns a dict_keys object
    person_keys = person.keys()
    print(person_keys)
    print(list(person_keys))

    # Iterating over the dictionary with items()
    for key, value in person.items():
        print(f"key={key}, value={value}")


if __name__ == "__main__":
    main()
