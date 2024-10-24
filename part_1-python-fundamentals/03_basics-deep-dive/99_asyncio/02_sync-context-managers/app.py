"""A basic sync context manager."""

from pathlib import Path
from typing import IO


class File:
    """File Context Manager."""

    def __init__(self, file_name: str, method: str) -> None:
        """Construct File Context Manager instance."""
        self.file_name = file_name
        self.method = method
        self.file_obj = None

    def __enter__(self) -> IO:
        """Perform the File object setup when entering the context manager."""
        self.file_obj = Path.open(Path(self.file_name), self.method)
        return self.file_obj

    def __exit__(self, type, value, traceback) -> bool | None:
        """Perform the File object teardown when exiting the context manager."""
        if value is not None:
            print(f"oops! an exception of type {type} occurred: {value!r}")
            print("Exception handled: won't be propagated")
        self.file_obj.close()  # type: ignore
        # if you comment the following line the exception will be bubbled up
        return True


def main() -> None:
    """Application entry point."""
    with File("my_file.txt", "w") as file:
        file.write("Hello to Jason Isaacs!")

    with File("my_file.txt", "r") as file:
        file.made_up_method("hello, hello!")  # type: ignore


if __name__ == "__main__":
    main()
