"""Illustrate how to access dict values with get and providing defaults."""


def main() -> None:
    """Application entry point."""
    person = {
        "name": "Idris",
        "age": 30,
    }

    print(f"Name: {person['name']}, age: {person['age']}")

    # Accessing a key that not exists raises a KeyError
    try:
        print(f"Nationality: {person['nationality']}")
    except KeyError:
        print("Oops! No nationality found")

    # You can use get to prevent that
    print(f"Nationality: {person.get('nationality')}")

    # And you can pass a second parameter to provide a default value
    print(f"Nationality: {person.get('nationality', 'N/A')}")


if __name__ == "__main__":
    main()
