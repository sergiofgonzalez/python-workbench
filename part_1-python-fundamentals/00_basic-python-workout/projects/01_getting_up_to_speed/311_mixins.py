"""A simple mixins example."""

import json
import pickle


class Person:
    """Represent a Person with name and age."""

    def __init__(self, name: str, age: int) -> None:
        """Initialize a Person instance."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """Developer-friendly representation of a Person."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class SerializerMixin:
    """Enhance a given class with serialization methods."""

    def to_json(self) -> str:
        """Serialize the instance as a JSON."""
        return json.dumps(self.__dict__)

    def to_csv(self) -> str:
        """Serialize the instance as a CSV."""
        return ",".join(str(value) for value in self.__dict__.values())

    def to_pickle(self) -> bytes:
        """Serialize the instance in Pickle format."""
        return pickle.dumps(self.__dict__)


class Employee(SerializerMixin, Person):
    """Represent an employee."""

    def __init__(self, name: str, age: int, employee_id: str, salary: float) -> None:
        """Initialize an employee instance."""
        super().__init__(name, age)
        self.employee_id = employee_id
        self.salary = salary


def main() -> None:
    """Application entry point."""
    employee = Employee("Alice", 30, "E123", 75000.0)
    print(f"{employee=}")
    print(f"{employee.to_json()=}")
    print(f"{employee.to_csv()=}")

    # print bytes in hex format
    employee_bytes = employee.to_pickle()
    print(f"{employee_bytes.hex()=}")


if __name__ == "__main__":
    main()
