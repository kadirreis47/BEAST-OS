from __future__ import annotations


class ContainerError(RuntimeError):
    """Base error raised by the dependency container."""


class ServiceNotRegisteredError(ContainerError):
    """Raised when a requested service has no registration."""


class CircularDependencyError(ContainerError):
    """Raised when a service resolution cycle is detected."""


class InvalidFactoryError(ContainerError):
    """Raised when a factory does not return the registered service type."""
