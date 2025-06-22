"""Illustrate the behavior of __dict__ in instances and classes."""

from pprint import pprint


class Duck:
    """Duck class with a constructor."""

    def __init__(self, name: str, color: str) -> None:
        """Initialize the Duck with a name."""
        self.name = name
        self.color = color

    def quack(self) -> str:
        """Return a quack sound."""
        return f"The {self.color} duck named {self.name} says Quack!"


def main() -> None:
    """Application entry point."""
    print("Duck class __dict__:")
    pprint(Duck.__dict__)

    print("\nDuck instance __dict__:")
    duck = Duck(name="Daffy", color="black")
    pprint(duck.__dict__)


if __name__ == "__main__":
    main()
