from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from threading import RLock
from types import MappingProxyType
from typing import Any

EventHandler = Callable[["Event"], None]


@dataclass(frozen=True, slots=True)
class Event:
    """Immutable domain event emitted inside BEAST OS."""

    name: str
    payload: dict[str, Any]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("event name must not be empty")
        object.__setattr__(self, "payload", MappingProxyType(dict(self.payload)))


class EventBus:
    """Thread-safe synchronous event dispatcher."""

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = defaultdict(list)
        self._lock = RLock()

    def subscribe(self, name: str, handler: EventHandler) -> None:
        if not name.strip():
            raise ValueError("event name must not be empty")
        if not callable(handler):
            raise TypeError("handler must be callable")
        with self._lock:
            if handler not in self._subscribers[name]:
                self._subscribers[name].append(handler)

    def unsubscribe(self, name: str, handler: EventHandler) -> bool:
        with self._lock:
            handlers = self._subscribers.get(name)
            if not handlers or handler not in handlers:
                return False
            handlers.remove(handler)
            if not handlers:
                self._subscribers.pop(name, None)
            return True

    def publish(self, event: Event) -> int:
        with self._lock:
            handlers = tuple(self._subscribers.get(event.name, ()))
        for handler in handlers:
            handler(event)
        return len(handlers)

    def subscriber_count(self, name: str) -> int:
        with self._lock:
            return len(self._subscribers.get(name, ()))
