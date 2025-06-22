"""Illustrate the basics of classes."""


class Duck:
    """A class representing a duck."""

    def quack(self) -> str:
        """Make the duck quack."""
        return "quack!"


def main() -> None:
    """Application entry point."""
    # Create an instance of Duck
    duck = Duck()

    # Call the quack method
    print(duck.quack())  # Output: quack!


if __name__ == "__main__":
    main()
