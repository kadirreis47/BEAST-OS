from __future__ import annotations


class CommandBusError(RuntimeError):
    """Base exception for command dispatch failures."""


class HandlerAlreadyRegisteredError(CommandBusError):
    """Raised when a command type already has a registered handler."""


class HandlerNotFoundError(CommandBusError):
    """Raised when no handler exists for a command type."""


class InvalidHandlerError(CommandBusError):
    """Raised when a registered handler cannot process commands."""
