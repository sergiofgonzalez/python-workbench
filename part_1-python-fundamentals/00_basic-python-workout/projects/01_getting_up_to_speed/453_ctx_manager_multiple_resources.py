"""Illustrates how to use context managers with multiple resources."""

from pathlib import Path
from types import TracebackType

in_base_path = Path("data", "in_data", "tasks")
out_base_path = Path("data", "out_data", "tmp")


class MyContextManager:
    """A simple context manager for demonstration purposes."""

    def __init__(self, name: str) -> None:
        """Initialize the context manager with a name."""
        self.name = name

    def __enter__(self) -> "MyContextManager":
        """Enter the context."""
        print(f"Entering context: {self.name}")
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context."""
        print(f"Exiting context: {self.name}")


def main() -> None:
    """Application entry point."""
    input_file = in_base_path / "tasks.csv"
    output_file = out_base_path / "tasks_copy.csv"

    with (
        input_file.open("r", encoding="utf-8") as infile,
        output_file.open("w", encoding="utf-8") as outfile,
    ):
        for line in infile:
            outfile.write(line)

    print(f"Copied data from {input_file} to {output_file}")
    print("=" * 40)

    # Demonstrate custom context managers
    with MyContextManager("Resource") as res:
        print("Using resources within the context: ", res.name)
    print("=" * 40)
    with MyContextManager("Resource1") as res1, MyContextManager("Resource2") as res2:
        print("Using resources within the context: ", res1.name)
        print("Using resources within the context: ", res2.name)
    print("=" * 40)


if __name__ == "__main__":
    main()
