"""Illustrates logging levels."""

import logging

logger = logging.getLogger(__name__)


def log_messages_at_all_levels() -> None:
    """Log messages at all levels."""
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


def main() -> None:
    """Application entry point."""
    for level in [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ]:
        logger.setLevel(level)
        print(f"\n=== Logging level set to {logging.getLevelName(level)} ===")
        log_messages_at_all_levels()

    # This doesn't work as expected because the default handler level is WARNING
    # and the log messages are filtered at the handler level first.
    for handler in logging.root.handlers:
        print(
            f"root handler before setting level: {handler}, "
            f"level={logging.getLevelName(handler.level)}",
        )

    # This doesn't work either, so it feels it needs to be set using the basicConfig


if __name__ == "__main__":
    main()
