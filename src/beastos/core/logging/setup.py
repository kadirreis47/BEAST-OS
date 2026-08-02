from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from typing import TextIO

from .formatter import JsonFormatter
from .redaction import RedactionFilter


@dataclass(frozen=True, slots=True)
class LoggingSettings:
    level: int | str = logging.INFO
    json_output: bool = True
    logger_name: str = "beastos"
    propagate: bool = False


def configure_logging(
    settings: LoggingSettings = LoggingSettings(),
    *,
    stream: TextIO | None = None,
) -> logging.Logger:
    logger = logging.getLogger(settings.logger_name)
    logger.setLevel(settings.level)
    logger.propagate = settings.propagate

    handler = logging.StreamHandler(stream or sys.stdout)
    handler.setLevel(settings.level)
    handler.addFilter(RedactionFilter())
    if settings.json_output:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))

    logger.handlers.clear()
    logger.addHandler(handler)
    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger("beastos" if not name else f"beastos.{name}")
