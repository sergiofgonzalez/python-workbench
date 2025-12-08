"""Illustrates how to redirect logs to file using a file handler."""

import logging

dst_file_path = "data/out_data/tmp/app.log"

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler(dst_file_path)
logger.addHandler(file_handler)


def main() -> None:
    """Application entry point."""
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    main()
