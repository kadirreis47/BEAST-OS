from __future__ import annotations

from collections.abc import Callable
from threading import RLock
from typing import Any, TypeVar, cast

from .contracts import QueryMiddleware
from .exceptions import (
    InvalidQueryHandlerError,
    QueryHandlerAlreadyRegisteredError,
    QueryHandlerNotFoundError,
)
from .models import Query

ResultT = TypeVar("ResultT")
QueryT = TypeVar("QueryT", bound=Query[Any])
Handler = Callable[[Query[Any]], object]


class QueryBus:
    """Thread-safe in-process query dispatcher with middleware support."""

    def __init__(self) -> None:
        self._handlers: dict[type[Query[Any]], Handler] = {}
        self._middleware: list[QueryMiddleware] = []
        self._lock = RLock()

    def register(
        self,
        query_type: type[QueryT],
        handler: Callable[[QueryT], ResultT],
        *,
        replace: bool = False,
    ) -> None:
        if not callable(handler):
            raise InvalidQueryHandlerError("Query handler must be callable.")

        with self._lock:
            if query_type in self._handlers and not replace:
                raise QueryHandlerAlreadyRegisteredError(
                    f"Handler already registered for {query_type.__name__}."
                )
            self._handlers[query_type] = cast(Handler, handler)

    def unregister(self, query_type: type[Query[Any]]) -> bool:
        with self._lock:
            return self._handlers.pop(query_type, None) is not None

    def use(self, middleware: QueryMiddleware) -> None:
        if not callable(middleware):
            raise TypeError("Query middleware must be callable.")
        with self._lock:
            self._middleware.append(middleware)

    def clear_middleware(self) -> None:
        with self._lock:
            self._middleware.clear()

    def registered_query_types(self) -> tuple[type[Query[Any]], ...]:
        with self._lock:
            return tuple(self._handlers)

    def ask(self, query: Query[ResultT]) -> ResultT:
        with self._lock:
            handler = self._handlers.get(type(query))
            middleware = tuple(self._middleware)

        if handler is None:
            raise QueryHandlerNotFoundError(
                f"No handler registered for {type(query).__name__}."
            )

        def invoke(current: Query[Any]) -> object:
            return handler(current)

        pipeline: Handler = invoke
        for item in reversed(middleware):
            next_handler = pipeline

            def wrapped(
                current: Query[Any],
                *,
                middleware_item: QueryMiddleware = item,
                call_next: Handler = next_handler,
            ) -> object:
                return middleware_item(current, call_next)

            pipeline = wrapped

        return cast(ResultT, pipeline(query))
