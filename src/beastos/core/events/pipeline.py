from __future__ import annotations

from collections.abc import Callable
from threading import RLock
from typing import TypeVar, cast

from .contracts import EventHandler, EventMiddleware
from .exceptions import (
    EventDispatchError,
    EventHandlerAlreadyRegisteredError,
    InvalidEventHandlerError,
)
from .models import DomainEvent

EventT = TypeVar("EventT", bound=DomainEvent)
TypedHandler = Callable[[EventT], None]


class DomainEventPipeline:
    """Thread-safe synchronous domain-event dispatcher."""

    def __init__(self) -> None:
        self._handlers: dict[type[DomainEvent], list[EventHandler]] = {}
        self._middleware: list[EventMiddleware] = []
        self._lock = RLock()

    def subscribe(
        self,
        event_type: type[EventT],
        handler: TypedHandler[EventT],
        *,
        allow_duplicate: bool = False,
    ) -> None:
        if not callable(handler):
            raise InvalidEventHandlerError("Event handler must be callable.")

        generic_handler = cast(EventHandler, handler)
        with self._lock:
            handlers = self._handlers.setdefault(event_type, [])
            if generic_handler in handlers and not allow_duplicate:
                raise EventHandlerAlreadyRegisteredError(
                    f"Handler already registered for {event_type.__name__}."
                )
            handlers.append(generic_handler)

    def unsubscribe(
        self,
        event_type: type[DomainEvent],
        handler: EventHandler,
    ) -> bool:
        with self._lock:
            handlers = self._handlers.get(event_type)
            if not handlers or handler not in handlers:
                return False
            handlers.remove(handler)
            if not handlers:
                self._handlers.pop(event_type, None)
            return True

    def use(self, middleware: EventMiddleware) -> None:
        if not callable(middleware):
            raise TypeError("Event middleware must be callable.")
        with self._lock:
            self._middleware.append(middleware)

    def clear(self) -> None:
        with self._lock:
            self._handlers.clear()
            self._middleware.clear()

    def handler_count(self, event_type: type[DomainEvent] | None = None) -> int:
        with self._lock:
            if event_type is not None:
                return len(self._handlers.get(event_type, ()))
            return sum(len(items) for items in self._handlers.values())

    def publish(self, event: DomainEvent, *, fail_fast: bool = True) -> int:
        with self._lock:
            handlers = tuple(self._resolve_handlers(type(event)))
            middleware = tuple(self._middleware)

        failures: list[BaseException] = []
        delivered = 0

        for handler in handlers:
            pipeline = self._build_pipeline(handler, middleware)
            try:
                pipeline(event)
                delivered += 1
            except BaseException as exc:  # preserve operational failures
                failures.append(exc)
                if fail_fast:
                    raise EventDispatchError(
                        f"Failed to dispatch {type(event).__name__}.",
                        tuple(failures),
                    ) from exc

        if failures:
            raise EventDispatchError(
                f"{len(failures)} handler(s) failed for {type(event).__name__}.",
                tuple(failures),
            )

        return delivered

    def _resolve_handlers(self, event_type: type[DomainEvent]) -> list[EventHandler]:
        resolved: list[EventHandler] = []
        for registered_type, handlers in self._handlers.items():
            if issubclass(event_type, registered_type):
                resolved.extend(handlers)
        return resolved

    @staticmethod
    def _build_pipeline(
        handler: EventHandler,
        middleware: tuple[EventMiddleware, ...],
    ) -> EventHandler:
        pipeline = handler
        for item in reversed(middleware):
            next_handler = pipeline

            def wrapped(
                event: DomainEvent,
                *,
                middleware_item: EventMiddleware = item,
                call_next: EventHandler = next_handler,
            ) -> None:
                middleware_item(event, call_next)

            pipeline = wrapped
        return pipeline
