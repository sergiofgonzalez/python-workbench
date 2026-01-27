"""Illustrate how to create a typed list by subclassing the UserList class."""

from collections import UserList
from typing import override


class TypedList(UserList):
    """A simple typed list that only elements of a given type."""

    def __init__(
        self,
        example_element: object,
        initial_items: list[object] | None = None,
    ) -> None:
        """Initialize the typed list with an example element to determine type."""
        self._element_type = type(example_element)
        initial_items = initial_items or []
        for item in initial_items:
            self._validate_type(item)
        super().__init__(initial_items)

    def _validate_type(self, item: object) -> None:
        """Validate that the item is of the correct type."""
        if not isinstance(item, self._element_type):
            msg = f"Item {item} is not of type {self._element_type.__name__}"
            raise TypeError(msg)

    @override
    def __setitem__(self, index: int, item: object) -> None:  # ty:ignore[invalid-method-override]
        """Set an item at a given index after validating its type."""
        self._validate_type(item)
        self.data[index] = item

    def __mul__(self, n: int) -> "TypedList":
        """Support list repetition (e.g., lst * n)."""
        return TypedList(
            example_element=self.data[0] if self.data else None,
            initial_items=self.data * n,
        )

    def __rmul__(self, n: int) -> "TypedList":
        """Support list repetition (e.g., n * lst)."""
        return self.__mul__(n)


class Person:
    """A simple Person class for demonstration purposes."""

    def __init__(self, name: str) -> None:
        """Initialize a Person with a name."""
        self.name = name

    def __repr__(self) -> str:
        """Return a string representation of the Person."""
        return f"Person(name={self.name})"


class Employee(Person):
    """An Employee class that inherits from Person."""

    def __init__(self, name: str, employee_id: int) -> None:
        """Initialize an Employee with a name and employee ID."""
        super().__init__(name)
        self.employee_id = employee_id

    def __repr__(self) -> str:
        """Return a string representation of the Employee."""
        return f"Employee(name={self.name}, employee_id={self.employee_id})"


def main() -> None:  # noqa: PLR0915
    """Application entry point."""
    # Initialization of a TypedList that only accepts strings
    tlist = TypedList("", 5 * [""])
    print(f"{tlist=}")
    print("-" * 40)

    # Setting items in the TypedList
    tlist[2] = "Hello"
    tlist[3] = "to"
    tlist[4] = "Jason Isaacs"
    print(f"{tlist=}")
    print("-" * 40)

    # Getting items in the TypedList
    print(f"{tlist[2]}-{tlist[3]}-{tlist[4]}")
    print("-" * 40)

    # Unpacking the elements of the TypedList
    a, b, c, d, e = tlist
    print(f"{a=}, {b=}, {c=}, {d=}, {e=}")
    print("-" * 40)

    # Iterating over the TypedList elements (note that we didn't implement __iter__!!!)
    for item in tlist:
        print(f"{item=}")
    print("-" * 40)

    # len() support
    tlist = TypedList("example")
    assert len(tlist) == 0

    # append() and len() support
    tlist.append("one")
    assert len(tlist) == 1
    assert tlist[0] == "one"

    # Deletion of an item
    del tlist[0]
    assert len(tlist) == 0
    print("-" * 40)

    # list concatenation support
    a = ["one", "two", "three"]
    b = ["four", "five"]
    print(f"Concatenation of {a} and {b}: {a + b}")

    x = TypedList("", ["uno", "dos", "tres"])
    y = TypedList("", ["cuatro", "cinco"])
    z = x + y
    print(
        f"Concatenation of {x} and {y}: {z} (type: {type(z).__name__})",
    )
    print("-" * 40)

    # list repetition support
    x = TypedList(0, [123])
    print(f"Original list: {x}")
    y = 5 * x
    print(f"Repeated list: {y}")
    y = x * 5
    print(f"Repeated list: {y}")
    print("-" * 40)

    # Let's now check the enforcement of types
    x = TypedList("", ["a", "b", "c"])
    try:
        x[0] = 123
    except TypeError as e:
        print(f"Caught an error while assigning an integer to a string TypedList: {e}")
    print("-" * 40)

    # What happens with subclasses?
    # float list will fail with integer items
    try:
        x = TypedList(0.1, [1, 2, 3])
    except TypeError as e:
        print(f"Caught an error while creating a float TypedList: {e}")
    print("-" * 40)

    # This works: Employee is a subclass of Person
    x = TypedList(Person("Example"), [Employee("Alice", 1), Person("Bob")])
    print(f"TypedList with Person and Employee: {x}")
    print("-" * 40)

    try:
        # This fails: Person is not a subclass of Employee
        x = TypedList(Employee("Example", 0), [Employee("Alice", 1), Person("Bob")])
    except TypeError as e:
        print(f"Caught an error while creating an Employee TypedList: {e}")
    print("-" * 40)


if __name__ == "__main__":
    main()
