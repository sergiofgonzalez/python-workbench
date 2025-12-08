"""TODO: description of the program."""

import logging

# Set logger level to DEBUG using basicConfig
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# File handler with WARNING level
file_handler = logging.FileHandler("data/out_data/tmp/app_warning.log")
file_handler.setLevel(logging.WARNING)
logger.addHandler(file_handler)

# File handler with CRITICAL level
file_handler = logging.FileHandler("data/out_data/tmp/app_critical.log")
file_handler.setLevel(logging.CRITICAL)
logger.addHandler(file_handler)

# Stream handler with INFO level
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


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

    logger.handlers.clear()
    print(f"Logging level set to {logging.getLevelName(logger.getEffectiveLevel())}")
    log_messages_at_all_levels()


if __name__ == "__main__":
    main()
