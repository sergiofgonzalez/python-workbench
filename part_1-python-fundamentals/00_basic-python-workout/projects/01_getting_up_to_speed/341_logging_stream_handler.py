"""Illustrates how to use a stream handler."""

import logging

stream_handler = logging.StreamHandler()
logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)


def main() -> None:
    """Application entry point."""
    logger.info("This is an info message")
    logger.debug("This is a debug message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # inspecting handlers
    for handler in logger.handlers:
        print(f"Handler: {handler}")

    # inspecting logging.root handlers
    for handler in logging.root.handlers:
        print(f"Root Handler: {handler}")


if __name__ == "__main__":
    main()
