from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Iterator

_context: ContextVar[dict[str, Any]] = ContextVar("beastos_log_context", default={})


def get_context() -> dict[str, Any]:
    return dict(_context.get())


def bind_context(**values: Any) -> None:
    merged = get_context()
    merged.update(values)
    _context.set(merged)


def clear_context(*keys: str) -> None:
    if not keys:
        _context.set({})
        return
    current = get_context()
    for key in keys:
        current.pop(key, None)
    _context.set(current)


@contextmanager
def logging_context(**values: Any) -> Iterator[None]:
    token = _context.set({**get_context(), **values})
    try:
        yield
    finally:
        _context.reset(token)
