"""Illustrates how to interpolate information in the log messages."""

import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S.%.3f",
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Application entry point."""
    name = "Alice"
    age = 30
    salary = 75000.123
    logger.info("User %s is %d years old and earns $%.3f", name, age, salary)
    logger.debug("Debugging user %s with age %d.", name, age)
    logger.warning("User %s has an age of %d, which is unusual.", name, age)
    logger.error("Error encountered for user %s aged %d.", name, age)
    logger.critical("Critical issue for user %s aged %d!", name, age)

if __name__ == "__main__":
    main()
