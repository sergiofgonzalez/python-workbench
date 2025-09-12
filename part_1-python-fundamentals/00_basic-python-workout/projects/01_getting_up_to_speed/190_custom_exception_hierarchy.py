"""Illustrates how to create your own exception hierarchy."""


class MyCustomError(Exception):
    """Base class for custom exceptions in this hierarchy."""


class MyFileExtensionError(MyCustomError):
    """Exception raised when an invalid file extension is encountered."""

    def __init__(self, filename: str) -> None:
        """Initialize the exception with the filename."""
        super().__init__()
        self.filename = filename

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        return f"The file {self.filename!r} is not a valid CSV file"


def main() -> None:
    """Application entry point."""
    try:
        raise MyFileExtensionError("log.txt")  # noqa: EM101
    except MyCustomError as e:
        print(f"An error occurred: {e} (exception type={type(e).__name__})")


if __name__ == "__main__":
    main()
