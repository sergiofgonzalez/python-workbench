"""Illustrates how to use logging.getLogger."""

import logging

logger = logging.getLogger(__name__)


def say_hello() -> object:
    """Log a hello message for the given name."""
    fun_logger = logging.getLogger(__name__)
    fun_logger.info("say_hello has been called")
    print("Hello, to Jason Isaacs!")
    return fun_logger


def multiply_2_by_3() -> object:
    """Return the product of a and b."""
    print("Multiplying 2 and 3")
    fun_logger = logging.getLogger(__name__)
    fun_logger.debug("Multiplying 2 and 3")
    return fun_logger


def main() -> None:
    """Application entry point."""
    assert logger is logging.getLogger(__name__)
    hello_logger = say_hello()
    multiply_logger = multiply_2_by_3()
    assert hello_logger is multiply_logger
    assert hello_logger is logger
    print("=== Loggers are the same instance ===")

    logger.info("This is an info message")  # this is suppressed by default
    logger.debug("This is a debug message")  # this is suppressed by default
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    main()
