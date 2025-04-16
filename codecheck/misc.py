import sys

from loguru import logger


def enable_trace():
    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    # logger.add("trace_long.log", level="TRACE")
