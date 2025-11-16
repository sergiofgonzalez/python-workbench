"""Illustrates how to check if a type is Hashable or not."""

from collections.abc import Hashable


class Person:
    """A simple class representing a person."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize the Person instance with a name and age."""
        self.name = name
        self.age = age


def is_hashable(obj: object) -> bool:
    """Check if the given object is hashable."""
    return isinstance(obj, Hashable)


def main() -> None:
    """Application entry point."""
    print(f"{is_hashable({'name': 'Jason Isaacs'})=}")
    print(f"{is_hashable([1, 2, 3])=}")
    print(f"{is_hashable({1, 2, 3})=}")
    print(f"{is_hashable(42)=}")
    print(f"{is_hashable('Hello, world!')=}")
    print(f"{is_hashable((1, 2, 3))=}")
    foo_bool = True
    print(f"{is_hashable(foo_bool)=}")
    print(f"{is_hashable(True)=}")  # noqa: FBT003
    print(f"{is_hashable(None)=}")
    print(f"{is_hashable(Person('John Doe', 30))=}")

    # Creating a report
    items = [
        {"name": "Jason Isaacs"},
        [1, 2, 3],
        {1, 2, 3},
        42,
        "Hello, world!",
        (1, 2, 3),
        foo_bool,
        True,
        None,
        Person("John Doe", 30),
    ]
    print("\n == Hashable Report ==")
    print(f"{'Data type':<15} Hashable (True/False)")
    for item in items:
        print(f"{type(item).__name__:<15} {is_hashable(item)}")


if __name__ == "__main__":
    main()
