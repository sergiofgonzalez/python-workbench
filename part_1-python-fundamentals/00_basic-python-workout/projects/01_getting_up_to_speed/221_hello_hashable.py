"""Illustrate how to use the built-in hash function."""


class Person:
    """A simple class representing a person."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize the Person instance with a name and age."""
        self.name = name
        self.age = age



def main() -> None:
    """Application entry point."""
    print(f"{hash('Hello, world!')=}")
    print(f"{hash(42)=}")
    print(f"{hash(Person('John Doe', 30))=}") # custom classes are hashable by default

    # unhashable types
    try:
        print(f"{hash([1, 2, 3])=}")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e} (type: {type(e).__name__})")

    try:
        print(f"{hash((1, 2, 3))=}")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e} (type: {type(e).__name__})")

    try:
        print(f"{hash({'name': 'Jason Isaacs'})=}")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e} (type: {type(e).__name__})")

    try:
        print(f"{hash({1, 2, 3})=}")
    except Exception as e:  # noqa: BLE001
        print(f"Error: {e} (type: {type(e).__name__})")




if __name__ == "__main__":
    main()
