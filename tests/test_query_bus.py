from __future__ import annotations

from dataclasses import dataclass

import pytest

from beastos.core.query import (
    Query,
    QueryBus,
    QueryHandlerAlreadyRegisteredError,
    QueryHandlerNotFoundError,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetScore(Query[int]):
    user_id: int


def test_dispatches_query_and_returns_typed_result() -> None:
    bus = QueryBus()
    bus.register(GetScore, lambda query: query.user_id * 10)

    assert bus.ask(GetScore(user_id=7)) == 70


def test_rejects_duplicate_handler_by_default() -> None:
    bus = QueryBus()
    bus.register(GetScore, lambda query: 1)

    with pytest.raises(QueryHandlerAlreadyRegisteredError):
        bus.register(GetScore, lambda query: 2)


def test_replace_overwrites_existing_handler() -> None:
    bus = QueryBus()
    bus.register(GetScore, lambda query: 1)
    bus.register(GetScore, lambda query: 2, replace=True)

    assert bus.ask(GetScore(user_id=1)) == 2


def test_missing_handler_raises_specific_error() -> None:
    bus = QueryBus()

    with pytest.raises(QueryHandlerNotFoundError):
        bus.ask(GetScore(user_id=1))


def test_unregister_returns_change_status() -> None:
    bus = QueryBus()
    bus.register(GetScore, lambda query: 1)

    assert bus.unregister(GetScore) is True
    assert bus.unregister(GetScore) is False


def test_middleware_wraps_handler_in_registration_order() -> None:
    bus = QueryBus()
    events: list[str] = []

    def first(query: Query[object], call_next):
        events.append("first:before")
        result = call_next(query)
        events.append("first:after")
        return result

    def second(query: Query[object], call_next):
        events.append("second:before")
        result = call_next(query)
        events.append("second:after")
        return result

    bus.use(first)
    bus.use(second)
    bus.register(GetScore, lambda query: events.append("handler") or 42)

    assert bus.ask(GetScore(user_id=1)) == 42
    assert events == [
        "first:before",
        "second:before",
        "handler",
        "second:after",
        "first:after",
    ]


def test_clear_middleware_keeps_handler_active() -> None:
    bus = QueryBus()
    calls: list[str] = []
    bus.use(lambda query, call_next: calls.append("middleware") or call_next(query))
    bus.clear_middleware()
    bus.register(GetScore, lambda query: 9)

    assert bus.ask(GetScore(user_id=1)) == 9
    assert calls == []


def test_registered_query_types_returns_snapshot() -> None:
    bus = QueryBus()
    bus.register(GetScore, lambda query: 1)

    assert bus.registered_query_types() == (GetScore,)
