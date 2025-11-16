"""Overriding Methods and Method Resolution Order (MRO) in Python OOP."""

from typing import override


class Employee:
    """Base class representing an employee."""

    def __init__(self, name: str, employee_id: str) -> None:
        """Initialize the employee with a name and ID."""
        self.name = name
        self.employee_id = employee_id

    def login(self) -> str:
        """Simulate employee login."""
        return f"Employee {self.name} (ID: {self.employee_id}) logged in."

    def logout(self) -> str:
        """Simulate employee logout."""
        return f"Employee {self.name} (ID: {self.employee_id}) logged out."


class Supervisor(Employee):
    """Subclass representing a supervisor, inheriting from Employee."""

    @override
    def login(self) -> str:
        """Override login method to include supervisor-specific behavior."""
        return f"Supervisor {self.name} (ID: {self.employee_id}) logged in."


class Subordinate(Employee):
    """Subclass representing a subordinate, inheriting from Employee."""


def main() -> None:
    """Application entry point."""
    supervisor = Supervisor("Alice", "S001")
    subordinate = Subordinate("Bob", "E001")

    print(supervisor.login())  # Calls overridden method in Supervisor
    print(supervisor.logout())  # Calls inherited method from Employee

    print(subordinate.login())  # Calls inherited method from Employee
    print(subordinate.logout())  # Calls inherited method from Employee
    print("===" * 10)
    # Display Method Resolution Order (MRO)
    print("Supervisor MRO:", [cls.__name__ for cls in Supervisor.mro()])
    print("Subordinate MRO:", [cls.__name__ for cls in Subordinate.mro()])


if __name__ == "__main__":
    main()
