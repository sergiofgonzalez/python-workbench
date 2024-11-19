"""mymod/mylib.py."""

from loguru import logger

# This is a good practice and will be appreciated by your lib consumers
logger.disable(__name__)

logger.info("This is an informational message from mylib")
logger.warning("This is a warning message from mylib")
logger.error("This is an error message from mylib")
logger.debug("This is a debug message from mylib")


def fn():
    logger.info("This is an informational message from mylib.fn")
    logger.warning("This is a warning message from mylib.fn")
    logger.error("This is an error message from mylib.fn")
    logger.debug("This is a debug message from mylib.fn")
