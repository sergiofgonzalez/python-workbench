"""Illustrate OOP inheritance and design principles."""


class Employee:
    """A simple employee class."""

    def __init__(self, name: str, employee_id: str) -> None:
        """Initialize the employee with a name and employee ID."""
        self.name = name
        self.employee_id = employee_id


class Supervisor(Employee):
    """A supervisor class that inherits from Employee."""

    def __init__(
        self, name: str, employee_id: str, subordinates: list[Employee] | None = None
    ) -> None:
        """Initialize the supervisor with a name, employee ID, and subordinates."""
        super().__init__(name, employee_id)
        self.subordinates = subordinates or []

    def supervise(self) -> str:
        """Return a string indicating supervision activity."""
        return (
            f"Supervisor {self.name} is supervising {len(self.subordinates)} employees."
        )


class Subordinate(Employee):
    """A subordinate class that inherits from Employee."""

    def __init__(self, name: str, employee_id: str, supervisor: Supervisor) -> None:
        """Initialize the subordinate with a name, employee ID, and supervisor."""
        super().__init__(name, employee_id)
        self.supervisor = supervisor

    def report(self) -> str:
        """Return a string indicating reporting activity."""
        return f"Subordinate {self.name} is reporting to Supervisor {self.supervisor.name}."


def main() -> None:
    """Application entry point."""
    supervisor = Supervisor("Alice", "S001")
    subordinate1 = Subordinate("Bob", "E001", supervisor)
    subordinate2 = Subordinate("Charlie", "E002", supervisor)

    supervisor.subordinates.extend([subordinate1, subordinate2])

    print(supervisor.supervise())
    print(subordinate1.report())
    print(subordinate2.report())


if __name__ == "__main__":
    main()
