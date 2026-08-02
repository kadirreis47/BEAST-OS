from dataclasses import dataclass

import pytest

from beastos.core.events import (
    DomainEvent,
    DomainEventPipeline,
    EventDispatchError,
    EventHandlerAlreadyRegisteredError,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class HabitCompleted(DomainEvent):
    habit_id: str


def test_publish_delivers_event() -> None:
    pipeline = DomainEventPipeline()
    received: list[str] = []
    pipeline.subscribe(HabitCompleted, lambda event: received.append(event.habit_id))

    delivered = pipeline.publish(HabitCompleted(habit_id="water"))

    assert delivered == 1
    assert received == ["water"]


def test_base_event_subscription_receives_subclasses() -> None:
    pipeline = DomainEventPipeline()
    received: list[str] = []
    pipeline.subscribe(DomainEvent, lambda event: received.append(type(event).__name__))

    pipeline.publish(HabitCompleted(habit_id="sleep"))

    assert received == ["HabitCompleted"]


def test_middleware_wraps_handler_in_registration_order() -> None:
    pipeline = DomainEventPipeline()
    order: list[str] = []

    def first(event, call_next):
        order.append("first-before")
        call_next(event)
        order.append("first-after")

    def second(event, call_next):
        order.append("second-before")
        call_next(event)
        order.append("second-after")

    pipeline.use(first)
    pipeline.use(second)
    pipeline.subscribe(HabitCompleted, lambda event: order.append("handler"))

    pipeline.publish(HabitCompleted(habit_id="focus"))

    assert order == [
        "first-before",
        "second-before",
        "handler",
        "second-after",
        "first-after",
    ]


def test_duplicate_handler_is_rejected() -> None:
    pipeline = DomainEventPipeline()

    def handler(event: HabitCompleted) -> None:
        pass

    pipeline.subscribe(HabitCompleted, handler)
    with pytest.raises(EventHandlerAlreadyRegisteredError):
        pipeline.subscribe(HabitCompleted, handler)


def test_unsubscribe_removes_handler() -> None:
    pipeline = DomainEventPipeline()

    def handler(event: HabitCompleted) -> None:
        pass

    pipeline.subscribe(HabitCompleted, handler)
    assert pipeline.unsubscribe(HabitCompleted, handler) is True
    assert pipeline.unsubscribe(HabitCompleted, handler) is False
    assert pipeline.handler_count() == 0


def test_fail_fast_wraps_handler_failure() -> None:
    pipeline = DomainEventPipeline()

    def broken(event: HabitCompleted) -> None:
        raise RuntimeError("boom")

    pipeline.subscribe(HabitCompleted, broken)

    with pytest.raises(EventDispatchError) as captured:
        pipeline.publish(HabitCompleted(habit_id="run"))

    assert len(captured.value.failures) == 1
    assert isinstance(captured.value.failures[0], RuntimeError)


def test_metadata_is_immutable_snapshot() -> None:
    source = {"source": "api"}
    event = HabitCompleted(habit_id="walk", metadata=source)
    source["source"] = "changed"

    assert event.metadata["source"] == "api"
    with pytest.raises(TypeError):
        event.metadata["source"] = "cli"  # type: ignore[index]
