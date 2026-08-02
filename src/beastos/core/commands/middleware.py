from __future__ import annotations

from typing import Any, Callable, Protocol

from .types import Command

NextHandler = Callable[[Command], Any]


class CommandMiddleware(Protocol):
    def __call__(self, command: Command, next_handler: NextHandler) -> Any:
        """Process a command and delegate to the next middleware."""
