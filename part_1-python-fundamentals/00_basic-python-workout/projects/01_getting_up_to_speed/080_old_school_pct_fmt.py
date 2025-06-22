"""Illustrate the syntax for the old-school string formatting using %."""


def birthday(name: str, age: int) -> str:
    """Return a birthday greeting using old-school formatting."""
    return "Hello to %s who turns %d tomorrow!" % (name, age)  # noqa: UP031

def main() -> None:
    """Application entry point."""
    print(birthday("Alice", 30))
    print(birthday("Bob", 25))


if __name__ == "__main__":
    main()
