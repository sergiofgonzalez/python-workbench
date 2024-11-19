"""Customizing the logger with `add`."""

import sys

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="INFO")

@logger.catch
def main() -> None:
    """Application entry point."""
    logger.info("This is an informational message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.debug("This is a debug message")


if __name__ == "__main__":
    main()
