"""A proxy that intercepts write calls to show on the screen what's being written."""

import typing


class WriteProxy:
    """Proxy that intercept write calls to log what's being written."""

    def __init__(self, file_obj: typing.TextIO) -> None:
        """Initialize a WriteProxy instance."""
        self._file_obj = file_obj

    def write(self, s: str) -> int:
        """Intercept the write call to print in stdout what's being written."""
        print(f"Writing: {s!r}")
        return self._file_obj.write(s)

    def writelines(self, lines: typing.Iterable[str]) -> None:
        """Delegate to the underlying file method."""
        return self._file_obj.writelines(lines)

    def flush(self) -> None:
        """Delegate to the underlying file method."""
        return self._file_obj.flush()

    def close(self) -> None:
        """Delegate to the underlying file method."""
        return self._file_obj.close()

    def __getattr__(self, name: str) -> typing.Any:
        """Delegate attribute access to the underlying file object."""
        return getattr(self._file_obj, name)
