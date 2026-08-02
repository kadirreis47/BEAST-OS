class DomainEventError(Exception):
    """Base exception for domain-event failures."""


class EventHandlerAlreadyRegisteredError(DomainEventError):
    """Raised when the same handler is registered more than once."""


class InvalidEventHandlerError(DomainEventError):
    """Raised when a handler is not callable."""


class EventDispatchError(DomainEventError):
    """Raised when one or more handlers fail during publication."""

    def __init__(self, message: str, failures: tuple[BaseException, ...]) -> None:
        super().__init__(message)
        self.failures = failures
