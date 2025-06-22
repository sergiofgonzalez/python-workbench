"""Illustrate the different techniques for defining getters and setters in Python."""


class Person1:
    """A class with a property using a getter and setter."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize the person with a name and age."""
        self._name = name
        self._age = age

    def set_name(self, name: str) -> None:
        """Set the name of the person."""
        self._name = name

    def get_name(self) -> str:
        """Get the name of the person."""
        return self._name

    def set_age(self, age: int) -> None:
        """Set the age of the person."""
        if age < 0:
            msg = "Age cannot be negative"
            raise ValueError(msg)
        self._age = age

    def get_age(self) -> int:
        """Get the age of the person."""
        return self._age

    def __repr__(self) -> str:
        """Return a string representation of the person."""
        return f"Person1(name={self._name}, age={self._age})"

    name = property(get_name, set_name, None, "The name of the person")
    age = property(get_age, set_age, None, "The age of the person")


class Person2:
    """A class with a property using the @property decorator."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize the person with a name and age."""
        self._name = name
        self._age = age

    @property
    def name(self) -> str:
        """Get the name of the person."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name of the person."""
        self._name = value

    @property
    def age(self) -> int:
        """Get the age of the person."""
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        """Set the age of the person."""
        if value < 0:
            msg = "Age cannot be negative"
            raise ValueError(msg)
        self._age = value

    def __repr__(self) -> str:
        """Return a string representation of the person."""
        return f"Person2(name={self._name}, age={self._age})"


def main() -> None:
    """Application entry point."""
    person1_obj = Person1("Alice", 30)
    print(person1_obj)
    print(f"Name: {person1_obj.name}, Age: {person1_obj.age}")
    person1_obj.name = "Bob"
    person1_obj.age = 25
    print(person1_obj)

    print("\nUsing Person2 with @property decorator:")
    person2_obj = Person2("Alice", 30)
    print(person2_obj)
    print(f"Name: {person2_obj.name}, Age: {person2_obj.age}")
    person2_obj.name = "Bob"
    person2_obj.age = 25
    print(person2_obj)


if __name__ == "__main__":
    main()
