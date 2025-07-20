"""Illustrate the use of the `is` operator."""


class Person:
    """A simple class to illustrate the use of the `is` operator."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person instance with name and age."""
        self.name = name
        self.age = age

    def __eq__(self, other: object) -> bool:
        """Check equality based on name and age."""
        if not isinstance(other, Person):
            return False
        return self.name == other.name and self.age == other.age

    def __repr__(self) -> str:
        """Return a string representation of the Person instance."""
        return f"Person(name={self.name!r}, age={self.age})"


def main() -> None:
    """Application entry point."""
    # using `is` to check identity of strings
    print("=== string identity ===")
    a = "hello"
    b = "hello"
    print(f"{a is b=}")  # True, because both refer to the same string object in memory
    print(f"{a == b=}")  # True, because the content is the same

    # using `is` to check identity of numbers
    print("\n=== number identity ===")
    x = 5
    y = 5
    print(f"{x is y=}")  # True, because small integers are cached in Python
    print(f"{x == y=}")  # True, because the value is the same

    # using `is` to check identity of booleans
    print("\n=== boolean identity ===")
    t1 = True
    t2 = True
    print(f"{t1 is t2=}")  # True, because True is a singleton in Python
    print(f"{t1 == t2=}")  # True, because the value is the same

    # using `is` to check identity of None
    print("\n=== None identity ===")
    n1 = None
    n2 = None
    print(f"{n1 is n2=}")  # True, because None is a singleton in Python
    print(f"{n1 == n2=}")  # True, because None is always equal to None

    # using `is` to check identity of lists
    print("\n=== list identity ===")
    list1 = [1, 2, 3]
    list2 = [1, 2, 3]
    print(f"{list1 is list2=}")  # False, because they are different
    print(f"{list1 == list2=}")  # True, because the content is

    # using `is` to check identity of custom objects
    print("\n=== custom object identity ===")
    person1 = Person("Alice", 30)
    person2 = Person("Alice", 30)
    print(f"{person1 is person2=}")  # False, because they are different
    print(f"{person1 == person2=}")  # False, because they are different


if __name__ == "__main__":
    main()
