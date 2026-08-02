from __future__ import annotations

import inspect
from threading import RLock
from typing import Any, TypeVar, cast, get_type_hints

from .exceptions import CircularDependencyError, InvalidFactoryError, ServiceNotRegisteredError
from .lifetime import Lifetime
from .registration import Factory, Registration

T = TypeVar("T")


class ServiceContainer:
    """Thread-safe dependency injection container with constructor injection."""

    def __init__(self) -> None:
        self._registrations: dict[type[Any], Registration] = {}
        self._resolution_stack: list[type[Any]] = []
        self._lock = RLock()

    def register_instance(self, service_type: type[T], instance: T) -> None:
        if not isinstance(instance, service_type):
            raise TypeError(f"instance must implement {service_type.__name__}")
        self._registrations[service_type] = Registration(
            service_type=service_type,
            factory=lambda _container: instance,
            lifetime=Lifetime.SINGLETON,
            instance=instance,
        )

    def register_factory(
        self,
        service_type: type[T],
        factory: Factory,
        *,
        lifetime: Lifetime = Lifetime.TRANSIENT,
    ) -> None:
        self._registrations[service_type] = Registration(
            service_type=service_type,
            factory=factory,
            lifetime=lifetime,
        )

    def register_type(
        self,
        service_type: type[T],
        implementation_type: type[T] | None = None,
        *,
        lifetime: Lifetime = Lifetime.TRANSIENT,
    ) -> None:
        implementation = implementation_type or service_type
        self.register_factory(
            service_type,
            lambda container: container._construct(implementation),
            lifetime=lifetime,
        )

    def resolve(self, service_type: type[T]) -> T:
        with self._lock:
            registration = self._registrations.get(service_type)
            if registration is None:
                raise ServiceNotRegisteredError(
                    f"Service is not registered: {service_type.__name__}"
                )

            if registration.lifetime is Lifetime.SINGLETON and registration.instance is not None:
                return cast(T, registration.instance)

            if service_type in self._resolution_stack:
                cycle = " -> ".join(
                    item.__name__ for item in [*self._resolution_stack, service_type]
                )
                raise CircularDependencyError(f"Circular dependency detected: {cycle}")

            self._resolution_stack.append(service_type)
            try:
                instance = registration.factory(self)
                if not isinstance(instance, service_type):
                    raise InvalidFactoryError(
                        f"Factory for {service_type.__name__} returned "
                        f"{type(instance).__name__}"
                    )
                if registration.lifetime is Lifetime.SINGLETON:
                    registration.instance = instance
                return cast(T, instance)
            finally:
                self._resolution_stack.pop()

    def contains(self, service_type: type[Any]) -> bool:
        return service_type in self._registrations

    def clear(self) -> None:
        with self._lock:
            self._registrations.clear()
            self._resolution_stack.clear()

    def _construct(self, implementation_type: type[T]) -> T:
        signature = inspect.signature(implementation_type.__init__)
        hints = get_type_hints(implementation_type.__init__)
        kwargs: dict[str, Any] = {}

        for name, parameter in signature.parameters.items():
            if name == "self" or parameter.kind in {
                inspect.Parameter.VAR_POSITIONAL,
                inspect.Parameter.VAR_KEYWORD,
            }:
                continue
            dependency_type = hints.get(name)
            if dependency_type is None:
                if parameter.default is not inspect.Parameter.empty:
                    continue
                raise TypeError(
                    f"Constructor parameter '{name}' on {implementation_type.__name__} "
                    "requires a type annotation"
                )
            kwargs[name] = self.resolve(dependency_type)

        return implementation_type(**kwargs)
