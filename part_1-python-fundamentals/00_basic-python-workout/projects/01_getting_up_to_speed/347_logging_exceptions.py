"""Illustrating logging exceptions and stack traces."""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
)


def main() -> None:
    """Application entry point."""
    logger = logging.getLogger(__name__)
    try:
        1 / 0  # type: ignore  # noqa: B018, PGH003
    except ZeroDivisionError:
        logger.exception("An exception occurred")

    logger.info("Continuing execution after the exception.")
    try:
        raise ValueError("An example value error")  # noqa: EM101, TRY003, TRY301
    except ValueError:
        logger.exception("An exception occurred")

    logger.info("Continuing execution after the exception.")


if __name__ == "__main__":
    main()
