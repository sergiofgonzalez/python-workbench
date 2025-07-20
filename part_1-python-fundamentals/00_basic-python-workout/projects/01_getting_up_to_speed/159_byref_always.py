"""Illustrates the fact that in Python everything is passed by ref."""


class Person:
    """A simple class to represent a person."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a person with a name and age."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Return a string representation of the person."""
        return f"Person(name={self.name}, age={self.age})"


MyType = int | float | str | tuple[int, int] | list | dict | Person


def change_value(x: MyType) -> None:
    """Change the value of x based on its type."""
    print(f"Original value and memory address: {x} 0x{id(x):x}")
    if isinstance(x, int):
        x = x + 1
    elif isinstance(x, float):
        x = x * 2.0
    elif isinstance(x, str):
        x = x.upper()
    elif isinstance(x, tuple):
        x = (x[0] + 1, x[1] + 1)
    elif isinstance(x, list):
        x[1] = "modified"
        x.append("new_item")
    elif isinstance(x, dict):
        x["new_key"] = "new_value"
    elif isinstance(x, Person):
        x.age += 1
        x.name = f"Mr./Ms. {x.name}"
    else:
        msg = f"Unsupported type: {type(x)}"
        raise TypeError(msg)
    print(f"Modified value and memory address: {x} 0x{id(x):x}")


def main() -> None:
    """Application entry point."""
    # change_value with integer
    # Note that the integer is immutable, so the original value remains unchanged
    # Within the function, a new integer is created, but it does not affect the original
    # so the original remains unchanged
    x = 42
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")
    print("=" * 40)

    # change_value with float
    # behaves like passed by value, since float is immutable
    x = 3.14
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")

    print("=" * 40)

    # change_value with string
    # behaves like passed by value, since string is immutable
    x = "hello"
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")

    print("=" * 40)

    # change_value with tuple
    # behaves like passed by value, since tuple is immutable
    x = (1, 2)
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")

    print("=" * 40)

    # change_value with list
    # behaves like passed by reference, since list is mutable
    # the original list is modified in place
    # so the original remains unchanged
    x = [1, None, 2, None, 3]
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")

    print("=" * 40)

    # change_value with dict
    # behaves like passed by reference, since dict is mutable
    # the original dict is modified in place
    x = {"key1": "value1", "key2": "value2"}
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")

    print("=" * 40)

    # change_value with Person
    # behaves like passed by reference, since Person is mutable
    x = Person(name="Alice", age=30)
    print(f"Before change_value: {x} 0x{id(x):x}")
    change_value(x)
    print(f"After change_value: {x} 0x{id(x):x}")


if __name__ == "__main__":
    main()
