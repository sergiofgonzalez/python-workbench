"""Log config utility"""

import logging
import os
import sys

from uvicorn.logging import DefaultFormatter

LOG_LEVEL = os.getenv("CRYPTID_LOG_LEVEL", logging.getLevelName(logging.INFO))

_uvicorn_default_formatter = DefaultFormatter(
    "{levelprefix:<8} {name} : {message}", style="{", use_colors=True
)


def _get_stream_handler(formatter):
    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_logger(
    name: str, *, formatter: logging.Formatter = _uvicorn_default_formatter
):
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    logger.addHandler(_get_stream_handler(formatter))
    return logger
