"""Customizing the logger with `add`."""

import sys

from loguru import logger

from mymod import mylib

logger.remove()
logger.add(sys.stderr, level="INFO")


@logger.catch
def main() -> None:
    """Application entry point."""
    logger.info("This is an informational message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.debug("This is a debug message")
    mylib.fn() # will display nothing as logging was disabled in the library

    # if we feel there's a prob in the library, we can enable the logging
    print(">> 2nd time")
    logger.enable("mymod")
    mylib.fn()


if __name__ == "__main__":
    main()
