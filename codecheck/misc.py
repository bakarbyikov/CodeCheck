import sys
from pathlib import Path

from loguru import logger

logger.remove()
logger.add(sys.stderr, level="TRACE")
logger.add("trace_long.log", level="TRACE")


def try_read(path: Path) -> str | None:
    try:
        return path.read_text()
    except FileNotFoundError:
        return None
