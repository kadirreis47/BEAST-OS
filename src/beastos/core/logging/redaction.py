from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from typing import Any

_DEFAULT_KEYS = frozenset({
    "authorization", "cookie", "password", "secret", "token", "api_key",
    "access_token", "refresh_token", "client_secret",
})


def redact(value: Any, sensitive_keys: frozenset[str] = _DEFAULT_KEYS) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): "***REDACTED***" if str(key).lower() in sensitive_keys else redact(item, sensitive_keys)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [redact(item, sensitive_keys) for item in value]
    return value


class RedactionFilter(logging.Filter):
    def __init__(self, sensitive_keys: frozenset[str] | None = None) -> None:
        super().__init__()
        self.sensitive_keys = sensitive_keys or _DEFAULT_KEYS

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, Mapping):
            record.msg = redact(record.msg, self.sensitive_keys)
        if hasattr(record, "event_data"):
            record.event_data = redact(record.event_data, self.sensitive_keys)
        return True
