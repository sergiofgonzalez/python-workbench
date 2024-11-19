"""Hello loguru."""
from loguru import logger


def main() -> None:
    """Application entry point."""
    logger.debug("Hello, loguru!")


if __name__ == "__main__":
    main()
