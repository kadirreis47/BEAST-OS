from __future__ import annotations

from abc import ABC, abstractmethod

import pytest

from beastos.core.container import (
    CircularDependencyError,
    InvalidFactoryError,
    Lifetime,
    ServiceContainer,
    ServiceNotRegisteredError,
)


class Clock(ABC):
    @abstractmethod
    def now(self) -> str: ...


class FixedClock(Clock):
    def now(self) -> str:
        return "08:00"


class MorningService:
    def __init__(self, clock: Clock) -> None:
        self.clock = clock


class A:
    def __init__(self, b: B) -> None:
        self.b = b


class B:
    def __init__(self, a: A) -> None:
        self.a = a


def test_constructor_injection() -> None:
    container = ServiceContainer()
    container.register_type(Clock, FixedClock, lifetime=Lifetime.SINGLETON)
    container.register_type(MorningService)

    service = container.resolve(MorningService)

    assert service.clock.now() == "08:00"


def test_singleton_lifetime() -> None:
    container = ServiceContainer()
    container.register_type(Clock, FixedClock, lifetime=Lifetime.SINGLETON)

    assert container.resolve(Clock) is container.resolve(Clock)


def test_transient_lifetime() -> None:
    container = ServiceContainer()
    container.register_type(Clock, FixedClock)

    assert container.resolve(Clock) is not container.resolve(Clock)


def test_instance_registration() -> None:
    container = ServiceContainer()
    clock = FixedClock()
    container.register_instance(Clock, clock)

    assert container.resolve(Clock) is clock


def test_unregistered_service() -> None:
    with pytest.raises(ServiceNotRegisteredError):
        ServiceContainer().resolve(Clock)


def test_circular_dependency_detection() -> None:
    container = ServiceContainer()
    container.register_type(A)
    container.register_type(B)

    with pytest.raises(CircularDependencyError, match="A -> B -> A"):
        container.resolve(A)


def test_invalid_factory_result() -> None:
    container = ServiceContainer()
    container.register_factory(Clock, lambda _container: object())

    with pytest.raises(InvalidFactoryError):
        container.resolve(Clock)
