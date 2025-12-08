"""Setting the logger format for a handler with logging.Formatter."""

import logging

# Python standard logging is super frustrating! You have to set levels
# both on the logger and on the handler, otherwise it doesn't work
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s : %(message)s")
stream_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)


def log_messages_at_all_levels() -> None:
    """Log messages at all levels."""
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


def main() -> None:
    """Application entry point."""
    print(f"Logging level set to {logging.getLevelName(logger.getEffectiveLevel())}")
    log_messages_at_all_levels()
    print("=" * 40)


if __name__ == "__main__":
    main()
