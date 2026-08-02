from __future__ import annotations

from collections.abc import Callable
from threading import RLock
from typing import Any

from .exceptions import TaskAlreadyRegisteredError, TaskNotFoundError

TaskHandler = Callable[[dict[str, Any]], None]


class TaskRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, TaskHandler] = {}
        self._lock = RLock()

    def register(self, name: str, handler: TaskHandler) -> None:
        if not name.strip():
            raise ValueError("handler name cannot be empty")
        with self._lock:
            if name in self._handlers:
                raise TaskAlreadyRegisteredError(name)
            self._handlers[name] = handler

    def unregister(self, name: str) -> None:
        with self._lock:
            if self._handlers.pop(name, None) is None:
                raise TaskNotFoundError(name)

    def resolve(self, name: str) -> TaskHandler:
        with self._lock:
            try:
                return self._handlers[name]
            except KeyError as exc:
                raise TaskNotFoundError(name) from exc

    def names(self) -> tuple[str, ...]:
        with self._lock:
            return tuple(sorted(self._handlers))
