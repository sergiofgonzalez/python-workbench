"""Illustrate the basics of type hints."""


class Greeter:
    """A simple class to greet users."""

    num_greetings: int = 0

    def say_hello(self, s: str) -> str:
        """Return a greeting message."""
        Greeter.num_greetings = Greeter.num_greetings + 1
        return f"Hello, {s}!"


def main() -> None:
    """Application entry point."""
    greeter = Greeter()
    print(greeter.say_hello("Alice"))  # Should print "Hello, Alice!"
    print(f"Number of greetings: {Greeter.num_greetings}")  # Should print 1

if __name__ == "__main__":
    main()
