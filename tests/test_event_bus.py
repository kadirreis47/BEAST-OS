from datetime import UTC

import pytest

from beastos.core.event_bus import Event, EventBus


def test_publish_delivers_immutable_event() -> None:
    bus = EventBus()
    received: list[int] = []
    bus.subscribe("metric.recorded", lambda event: received.append(event.payload["value"]))

    delivered = bus.publish(Event("metric.recorded", {"value": 42}))

    assert delivered == 1
    assert received == [42]


def test_unsubscribe_removes_handler() -> None:
    bus = EventBus()
    handler = lambda event: None
    bus.subscribe("x", handler)

    assert bus.unsubscribe("x", handler) is True
    assert bus.unsubscribe("x", handler) is False
    assert bus.subscriber_count("x") == 0


def test_event_uses_timezone_aware_unique_timestamp() -> None:
    first = Event("x", {})
    second = Event("x", {})

    assert first.created_at.tzinfo is UTC
    assert second.created_at >= first.created_at


def test_event_payload_cannot_be_mutated() -> None:
    event = Event("x", {"value": 1})

    with pytest.raises(TypeError):
        event.payload["value"] = 2
