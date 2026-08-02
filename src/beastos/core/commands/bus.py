from __future__ import annotations

from threading import RLock
from typing import Any, Iterable, TypeVar

from .errors import (
    HandlerAlreadyRegisteredError,
    HandlerNotFoundError,
    InvalidHandlerError,
)
from .middleware import CommandMiddleware, NextHandler
from .types import Command, CommandHandler

CommandType = TypeVar("CommandType", bound=Command)


class CommandBus:
    """Thread-safe in-process command dispatcher with middleware support."""

    def __init__(self, middleware: Iterable[CommandMiddleware] = ()) -> None:
        self._handlers: dict[type[Command], CommandHandler[Any, Any]] = {}
        self._middleware = tuple(middleware)
        self._lock = RLock()

    def register(
        self,
        command_type: type[CommandType],
        handler: CommandHandler[CommandType, Any],
        *,
        replace: bool = False,
    ) -> None:
        if not isinstance(handler, CommandHandler):
            raise InvalidHandlerError("handler must expose a callable handle method")

        with self._lock:
            if command_type in self._handlers and not replace:
                raise HandlerAlreadyRegisteredError(
                    f"handler already registered for {command_type.__qualname__}"
                )
            self._handlers[command_type] = handler

    def unregister(self, command_type: type[Command]) -> bool:
        with self._lock:
            return self._handlers.pop(command_type, None) is not None

    def has_handler(self, command_type: type[Command]) -> bool:
        with self._lock:
            return command_type in self._handlers

    def dispatch(self, command: Command) -> Any:
        with self._lock:
            handler = self._handlers.get(type(command))

        if handler is None:
            raise HandlerNotFoundError(
                f"no handler registered for {type(command).__qualname__}"
            )

        def invoke(current: Command) -> Any:
            return handler.handle(current)

        chain: NextHandler = invoke
        for middleware in reversed(self._middleware):
            next_handler = chain

            def wrapped(
                current: Command,
                middleware: CommandMiddleware = middleware,
                next_handler: NextHandler = next_handler,
            ) -> Any:
                return middleware(current, next_handler)

            chain = wrapped

        return chain(command)
