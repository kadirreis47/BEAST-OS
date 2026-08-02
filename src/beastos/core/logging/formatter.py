from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from .context import get_context

_STANDARD_FIELDS = frozenset(logging.makeLogRecord({}).__dict__)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        payload.update(get_context())

        event_data = getattr(record, "event_data", None)
        if isinstance(event_data, dict):
            payload["data"] = event_data

        extras = {
            key: value
            for key, value in record.__dict__.items()
            if key not in _STANDARD_FIELDS and key not in {"message", "asctime", "event_data"}
        }
        if extras:
            payload["extra"] = extras

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False, default=str, separators=(",", ":"))
