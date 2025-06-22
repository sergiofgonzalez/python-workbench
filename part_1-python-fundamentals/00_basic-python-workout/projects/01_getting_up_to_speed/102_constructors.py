"""Class with constructor."""


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
    duck = Duck(name="Daffy", color="black")
    print(duck.quack())
    print(f"{duck.name=}, {duck.color=}")


if __name__ == "__main__":
    main()
