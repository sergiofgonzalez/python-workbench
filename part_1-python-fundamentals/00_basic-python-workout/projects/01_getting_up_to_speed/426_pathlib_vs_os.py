"""Illustrate some basic path operation example using pathlib and os."""

import os
from pathlib import Path


def main() -> None:
    """Application entry point."""
    # using os
    os_path = os.path.join("data", "out_data", "tmp", "test.log")  # noqa: PTH118
    basename, name = os.path.split(os_path)
    name += ".old"
    bkp_os_path = os.path.join(basename, name)  # noqa: PTH118
    print(f"os backup path: {bkp_os_path}")
    assert bkp_os_path == "data/out_data/tmp/test.log.old"

    # using pathlib
    path = Path("data") / "out_data" / "tmp" / "test.log"
    bkp_path = path.with_suffix(path.suffix + ".old")
    print(f"pathlib backup path: {bkp_path}")
    assert str(bkp_path) == "data/out_data/tmp/test.log.old"


if __name__ == "__main__":
    main()
