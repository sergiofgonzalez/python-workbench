"""Illustrate the use of `type()` to get the type of an object."""


class Person:
    """A simple class to represent a person."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person with a name and age."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Return a string representation of the Person."""
        return f"Person(name={self.name}, age={self.age})"


def main() -> None:
    """Application entry point."""
    print(type(42))  # noqa: UP003
    print(type("Hello, world!"))  # noqa: UP003
    print(type([1, 2, 3]))
    print(type(Person("Alice", 30)))
    print(type(None))
    print(type(main))
    print(type(Person))
    print(type(3.14))  # noqa: UP003
    print(type({"key": "value"}))
    print(type((1, 2, 3)))


if __name__ == "__main__":
    main()
