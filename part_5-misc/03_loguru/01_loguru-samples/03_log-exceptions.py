"""Customizing the logger with `add`."""

from loguru import logger


def carny_shotgun() -> None:
    """Raise an exception when invoked."""
    err_msg = "Fabricated exception!"
    raise NotImplementedError(err_msg)


@logger.catch
def main() -> None:
    """Application entry point."""
    logger.info("This program fails like a carny shotgun")
    carny_shotgun()
    logger.info("yay!")


if __name__ == "__main__":
    main()
