"""Illustrate how to patch dict-like objects."""

import os
from unittest.mock import patch


def main() -> None:
    """Application entry point."""
    print("Original PATH:", os.environ.get("PATH"))
    with patch.dict(os.environ, {"PATH": "/mocked/path"}):
        print("Mocked PATH:", os.environ.get("PATH"))
    print("Restored PATH:", os.environ.get("PATH"))


if __name__ == "__main__":
    main()
