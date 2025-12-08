"""Setting the logger format when using basicConfig."""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
)


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
    print(f"Logging level set to {logging.getLevelName(logger.getEffectiveLevel())}")
    log_messages_at_all_levels()
    print("=" * 40)


if __name__ == "__main__":
    main()
