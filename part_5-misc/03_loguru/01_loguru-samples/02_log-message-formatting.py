"""Customizing the logger with `add`."""

from loguru import logger


def main() -> None:
    """Application entry point."""
    logger.info(
        "If using {}, use at least {version}",
        "Python",
        version="3.12.5",
    )


if __name__ == "__main__":
    main()
