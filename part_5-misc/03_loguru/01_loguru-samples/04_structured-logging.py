"""Customizing the logger with `add`."""

import sys
from loguru import logger

logger.add(sys.stderr, serialize=True)


@logger.catch
def main() -> None:
    """Application entry point."""
    logger.info(
        "If using {}, use at least {version}",
        "Python",
        version="3.12.5",
    )


if __name__ == "__main__":
    main()
