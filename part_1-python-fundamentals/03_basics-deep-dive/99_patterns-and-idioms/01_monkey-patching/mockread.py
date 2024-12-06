"""Path.readlines monkey patching."""

import types
from pathlib import Path

OriginalPathOpen = Path.open


def enable_mock(respond_with: str) -> None:
    """Activate the monkey patching with the given canned response."""
    Path.open = lambda *_: MockedFile(respond_with)


def disable_mock() -> None:
    """Deactivate the monkey patching with the given canned response."""
    Path.open = OriginalPathOpen


class MockedFile:
    """Monkey patching of the file object returned by Pathlib."""

    def __init__(self, mocked_response: str) -> None:
        """Initialize the mocked file object."""
        self.mocked_response = mocked_response

    def __enter__(self) -> "MockedFile":
        """Tasks upon entering the context manager."""
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_traceback: types.TracebackType | None,
    ) -> None:
        """Tasks upon exiting the context manager."""

    def read(self) -> str:
        """Return the canned response."""
        return self.mocked_response
