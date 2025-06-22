"""Illustrate how to use `sorted()` to sort objects with a custom function."""


class Person:
    """A simple class representing a person."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a person with a name and age."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Return a string representation of the person."""
        return f"Person(name={self.name}, age={self.age})"

    def __str__(self) -> str:
        """Return a user-friendly string representation of the person."""
        return f"{self.name} ({self.age} years old)"


def main() -> None:
    """Application entry point."""
    """Sort a list of Person objects by age using a custom function."""
    people = [
        Person("Alice", 30),
        Person("Bob", 25),
        Person("Charlie", 35),
    ]
    print(f"Unsorted people: {people}")

    # Sorting the list of people by age
    sorted_people = sorted(people, key=lambda person: person.age)
    print(f"Sorted people by age: {sorted_people}")

    # Verifying that the original list is unchanged
    assert people != sorted_people, "The original list should not be modified."
    print("Original list remains unchanged.")


if __name__ == "__main__":
    main()
