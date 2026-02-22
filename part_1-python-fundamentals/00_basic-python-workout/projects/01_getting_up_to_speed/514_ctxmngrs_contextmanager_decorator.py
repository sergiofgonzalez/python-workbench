"""Illustrates how to create a context manager using the contextlib.contextmanager decorator."""
from contextlib import contextmanager
import rich

@contextmanager
def my_context_manager(num: int):
    rich.print("[yellow]>>> Entering the context[/yellow]")
    yield num
    rich.print("[yellow]>>> Exiting the context[/yellow]")


def main() -> None:
    """Application entry point."""
    with my_context_manager(42) as value:
        print(f"Inside the context, value is: {value}")


if __name__ == "__main__":
    main()
