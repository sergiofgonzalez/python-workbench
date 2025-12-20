"""Illustrates that mutable tuples cannot be used as dict keys (among others)."""

from collections.abc import Hashable


class Person:
    """Simple Person class for demonstration."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize Person with name and age."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Return string representation of Person."""
        return f"Person(name={self.name}, age={self.age})"


class PersonV2:
    """Simple Person class with overridden __hash__."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize Person with name and age."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Return string representation of Person."""
        return f"PersonV2(name={self.name}, age={self.age})"

    def __hash__(self) -> int:
        """Override hash to make object unhashable."""
        msg = "unhashable type: 'PersonV2'"
        raise TypeError(msg)


class PersonV3:
    """Simple Person class with custom __hash__."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize Person with name and age."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Return string representation of Person."""
        return f"PersonV3(name={self.name}, age={self.age})"

    def __hash__(self) -> int:
        """Compute custom hash based on name and age."""
        return hash((self.name, self.age))


def main() -> None:
    """Application entry point."""
    # tuple with immutable elements can be used as dict key
    t = (1, 2, 3, 4)
    d = {t: "immutable tuple as key"}
    print(d)

    # tuple with mutable elements cannot be used as dict key
    t2 = (1, 2, [3, 4])
    try:
        d = {t2: "mutable tuple as key"}
    except TypeError as e:
        print(f"Error: {e}")

    # Checking hashability with 'Hashable' is not a good idea
    # as tuples with mutable elements are still instances of 'Hashable'
    # but they will raise TypeError when used as dict keys at runtime.
    if isinstance(t, Hashable):
        print("t is hashable")
    else:
        print("t is not hashable")

    if isinstance(t2, Hashable):
        print("t2 is hashable")
    else:
        print("t2 is not hashable")

    # t2.__hash__() will raise TypeError
    try:
        print(t2.__hash__())
    except TypeError as e:
        print(f"Error: {e}")

    # Custom objects are hashable by default unless __hash__ is overridden
    alice = Person("Alice", 30)
    d = {alice: "Person object as key"}
    print(f"{alice}, {alice.__hash__()=}")

    # Even if we modify the object's attributes, its hash remains the same
    alice.name = "Alicia"
    print(f"After modifying name: {alice}, {alice.__hash__()=}")
    print(d)

    # Now with PersonV2 which overrides __hash__ to raise TypeError
    bob = PersonV2("Bob", 25)
    try:
        d = {bob: "PersonV2 object as key"}
    except TypeError as e:
        print(f"Error: {e}")

    # Now with PersonV3 which has a custom __hash__ implementation
    charlie = PersonV3("Charlie", 40)
    d = {charlie: "PersonV3 object as key"}
    print(f"{charlie}, {charlie.__hash__()=}")

    charlie.age = 41  # modifying attribute
    print(f"After modifying age: {charlie}, {charlie.__hash__()=}")
    print(d)

    try:
        print(d[charlie])  # This will not work because the hash has changed
    except KeyError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
