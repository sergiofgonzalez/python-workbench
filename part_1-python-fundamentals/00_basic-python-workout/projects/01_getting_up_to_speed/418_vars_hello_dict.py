"""Using vars() to convert an object's __dict__ attribute to a dictionary."""

from __future__ import annotations


class Employee:
    """Simple Employee class."""

    def __init__(
        self,
        employee_id: str,
        name: str,
        age: int,
        supervisor: Employee | None,
        salary: float,
    ) -> None:
        """Initialize an Employee instance."""
        self.employee_id: str = employee_id
        self.name = name
        self.age = age
        self.supervisor: Employee = supervisor
        self.salary: float = salary


def main() -> None:
    """Application entry point."""
    # Create an Employee instance
    alice = Employee(
        employee_id="E001",
        name="Alice Smith",
        age=30,
        supervisor=None,
        salary=75000.0,
    )

    # Iterate over the attributes using vars()
    print("Using vars():")
    for attr_name, attr_value in vars(alice).items():
        print(f"{attr_name}: {attr_value}")
    print("=" * 40)

    # Iterate over the attributes using __dict__ (equivalent to vars() but uglier)
    print("Using __dict__:")
    for attr_name, attr_value in alice.__dict__.items():
        print(f"{attr_name}: {attr_value}")
    print("=" * 40)

    # However, accessing __dict__ directly might be clearer in some contexts
    print(f"Employee ID accessed directly: {alice.__dict__['employee_id']}")
    print(f"Name accessed through vars(): {vars(alice)['name']}")


if __name__ == "__main__":
    main()
