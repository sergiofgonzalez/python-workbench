"""Illustrates how to create a file context manager using classes."""

from pathlib import Path
from typing import IO, TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

import logging

logging.basicConfig(level="DEBUG", format="%(asctime)s [%(levelname)-5s]  %(message)s")
logger = logging.getLogger(__name__)

base_path = Path("data", "out_data", "tmp")


class FileContextManager:
    """A context manager for handling file operations."""

    def __init__(self, filename: Path | str, mode: str) -> None:
        """Initialize with the filename and mode."""
        logger.debug(
            "Initializing FileContextManager with file: %s, mode: %s",
            filename,
            mode,
        )
        self.file_path = Path(filename)
        self.mode = mode
        self.file = None

    def __enter__(self) -> IO:
        """Open the file and return the file object."""
        logger.debug("Entering context: opening file %s", self.file_path)
        self.file = self.file_path.open(self.mode)
        return self.file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Close the file."""
        logger.debug("Exiting context: closing file %s", self.file_path)
        if exc_type is not None:
            logger.error(
                "__exit__: Exception received: %s (type: %s)",
                exc_value,
                exc_type,
            )
            logger.error("__exit__: Traceback: %s", traceback)
            logger.info("__exit__: Exceptions other than IOError are not handled.")
            if issubclass(exc_type, IOError):
                logger.info("__exit__: Suppressing IOError exception.")
                return True  # Suppress IOError exceptions
        else:
            logger.debug("__exit__: No exceptions occurred.")
        if self.file:
            logger.debug("__exit__: Closing file %s", self.file_path)
            self.file.close()
        return None  # Do not suppress exceptions


def main() -> None:
    """Application entry point."""
    file_path = base_path / "example.txt"

    # Write operations using the FileContextManager
    with FileContextManager(file_path, "w") as file:
        file.write("Hello, World!\n")
        file.write("This is a test of the FileContextManager.\n")
    logger.info("File operations completed.")
    print("=" * 40)

    # Read operations using the FileContextManager
    with FileContextManager(file_path, "r") as file:
        for i, line in enumerate(file, start=1):
            print(f"Line {i}: {line.strip()}")
    print("=" * 40)

    # Demonstrate exception handling:
    # scenario 1: exception raised in consumer code within the context
    # with propagation in __exit__
    try:
        with FileContextManager(file_path, "r") as file:
            msg = "This is a test exception."
            raise ValueError(msg)  # noqa: TRY301
    except ValueError:
        logger.exception("main(): Caught an exception")
    print("=" * 40)

    # Demonstrate exception handling:
    # scenario 2: exception raised with the context manager class itself
    # attempting to open a non-existent file
    # This will fail in __enter__ and __exit__ will not be called
    try:
        with FileContextManager(base_path / "non_existent_file.txt", "r") as file:
            file.read()
    except Exception:
        logger.exception("main(): Caught an exception")
    print("=" * 40)

    # Demonstrate exception handling:
    # scenario 3: exception raised by 3rd party code in consumer code
    # within the context without suppression in __exit__
    try:
        with FileContextManager(base_path / "non_existent_file.txt", "w") as file:
            # non existent method to raise an exception
            file.squeeze()  # ty:ignore[unresolved-attribute]
    except Exception:
        logger.exception("main(): Caught an exception")
    print("=" * 40)

    # Demonstrate exception handling:
    # scenario 4: exception raised in consumer code within the context
    # with suppression in __exit__
    try:
        with FileContextManager(file_path, "r") as file:
            msg = "This is a test exception."
            raise IOError(msg)  # noqa: TRY301, UP024
    except Exception:
        logger.exception("main(): Caught an exception")
    print("=" * 40)


if __name__ == "__main__":
    main()
