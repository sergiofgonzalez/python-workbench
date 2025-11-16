"""Illustrates how to override a subclass method and invoke the superclass method."""

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

    def __init__(self, name: str, employee_id: str) -> None:
        """Initialize Supervisor instance."""
        # invokes the superclass initializer as first statement
        supervisor_name = "Supervisor " + name
        super().__init__(supervisor_name, employee_id)

    @override
    def login(self) -> str:
        """Override login method to include supervisor-specific behavior."""
        return f"Supervisor {self.name} (ID: {self.employee_id}) logged in."

    @override
    def logout(self) -> str:
        print(f"logging out: {self.name}")
        base_logout = super().logout()  # Call the superclass method as first statement
        return f"{base_logout} (Supervisor privileges revoked.)"


def main() -> None:
    """Application entry point."""
    alice = Employee("alice", "001")
    bob = Supervisor("Bob", "002")

    print(alice.login())
    print(alice.logout())
    print(bob.login())
    print(bob.logout())


if __name__ == "__main__":
    main()
