"""Illustrates how to create custom context managers."""

import logging
from io import TextIOWrapper
from pathlib import Path
from types import TracebackType

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


class BasicTextFileReader:
    """A basic context manager for reading text files."""

    def __init__(
        self,
        file_path: str,
        *,
        should_suppress_exceptions: bool = True,
        should_raise_on_open: bool | None = None,
        should_raise_on_exit: bool | None = None,
    ) -> None:
        """Initialize the context manager with the file path."""
        self.file_path = file_path
        self.should_raise_on_open = should_raise_on_open
        self.should_raise_on_exit = should_raise_on_exit
        self.should_suppress_exceptions = should_suppress_exceptions
        self.file = None

    def __enter__(self) -> TextIOWrapper:
        """Open the file and return the file object."""
        logger.debug("In __enter__: Opening file: %s", self.file_path)
        self.file = Path(self.file_path).open("r", encoding="utf-8")
        if self.should_raise_on_open:
            logger.debug("In __enter__: Raising exception as requested.")
            msg = "Exception raised during __enter__"
            raise RuntimeError(msg)
        return self.file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        """Close the file."""
        logger.debug("In __exit__: Closing file: %s", self.file_path)
        if self.should_raise_on_exit:
            logger.debug("In __exit__: Raising exception as requested.")
            msg = "Exception raised during __exit__"
            raise RuntimeError(msg)
        if self.file:
            self.file.close()
        logger.debug("In __exit__: About to return %s", self.should_suppress_exceptions)
        return self.should_suppress_exceptions  # Suppress exceptions (if any)


def main() -> None:  # noqa: PLR0915
    """Application entry point."""
    with BasicTextFileReader("999_template.py") as text_file:
        content = text_file.read()
        print(content)
    print("=" * 40)
    with BasicTextFileReader("999_template.py") as text_file:
        for line in text_file:
            print(line.rstrip())
    print("=" * 40)

    # Testing exception handling
    # 1. Suppress exceptions when file does not exist
    # Exception is not suppressed
    try:
        with BasicTextFileReader("non_existent_file.txt") as text_file:
            content = text_file.read()
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 2. Do not suppress exceptions when file does not exist
    # Exception is raised
    try:
        with BasicTextFileReader(
            "non_existent_file.txt",
            should_suppress_exceptions=False,
        ) as text_file:
            content = text_file.read()
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 3. Suppress exception during enter
    # Exception is raised
    try:
        with BasicTextFileReader(
            "999_template.py",
            should_suppress_exceptions=True,
            should_raise_on_open=True,
        ) as text_file:
            content = text_file.read()
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 4. Don't suppress exception during enter
    # Exception is raised
    try:
        with BasicTextFileReader(
            "999_template.py",
            should_suppress_exceptions=False,
            should_raise_on_open=True,
        ) as text_file:
            content = text_file.read()
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 3. Suppress exception during exit
    # Exception is raised
    try:
        with BasicTextFileReader(
            "999_template.py",
            should_suppress_exceptions=True,
            should_raise_on_exit=True,
        ) as text_file:
            content = text_file.read()
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 4. Don't suppress exception during enter
    # Exception is raised
    try:
        with BasicTextFileReader(
            "999_template.py",
            should_suppress_exceptions=False,
            should_raise_on_exit=True,
        ) as text_file:
            content = text_file.read()
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 5. Suppress Exceptions when an exception is raised within the with block
    # Exception is suppressed, so suppression only works within the with block
    try:
        with BasicTextFileReader(
            "999_template.py",
            should_suppress_exceptions=True,
        ) as text_file:
            msg = "An error occurred within the with block"
            raise ValueError(msg)  # noqa: TRY301
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

    # 6. Don't suppress Exceptions when an exception is raised within the with block
    # Exception is not suppressed, so suppression only works within the with block
    try:
        with BasicTextFileReader(
            "999_template.py",
            should_suppress_exceptions=False,
        ) as text_file:
            msg = "An error occurred within the with block"
            raise ValueError(msg)  # noqa: TRY301
    except Exception as e:  # noqa: BLE001
        print(f"Exception was raised: {e} ({type(e).__name__})")
    print("=" * 40)

if __name__ == "__main__":
    main()
