"""Illustrate how to add support to with in custom classes."""

from pathlib import Path
from traceback import print_exception
from types import TracebackType
from typing import TextIO


class MessageWriter:
    """A class that writes messages to a file."""

    def __init__(self, file_path: Path | str) -> None:
        """Initialize the MessageWriter with a file path."""
        self.file_path = Path(file_path)
        self.file_obj = None

    def __enter__(self) -> TextIO:
        """Open the file and return the file object."""
        self.file_obj = self.file_path.open("w")
        return self.file_obj

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the file when exiting the context."""
        # print the exception type, value, and traceback if any
        if exc_type is not None:
            print(f"Exception type: {exc_type}")
            print(f"Exception value: {exc_value}")
            if traceback:
                print_exception(exc_type, exc_value, traceback)
        if self.file_obj:
            self.file_obj.close()


def main() -> None:
    """Application entry point."""
    with MessageWriter(
        "data/out_data/134_using_with_in_custom_classes/sample.txt",
    ) as writer:
        writer.write("This is a test message written using a custom context manager.\n")
        # Uncomment the next line to raise an exception and see how it is handled
        # raise ValueError("Fabricated exception to trigger__exit__.")  # noqa: ERA001


if __name__ == "__main__":
    main()
