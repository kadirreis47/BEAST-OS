from __future__ import annotations

from dataclasses import dataclass

import pytest

from beastos.core.commands import (
    Command,
    CommandBus,
    HandlerAlreadyRegisteredError,
    HandlerNotFoundError,
    InvalidHandlerError,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AddPoints(Command):
    user_id: str
    amount: int


class AddPointsHandler:
    def __init__(self) -> None:
        self.total = 0

    def handle(self, command: AddPoints) -> int:
        self.total += command.amount
        return self.total


def test_dispatches_to_registered_handler() -> None:
    handler = AddPointsHandler()
    bus = CommandBus()
    bus.register(AddPoints, handler)

    result = bus.dispatch(AddPoints(user_id="u-1", amount=5))

    assert result == 5
    assert handler.total == 5


def test_rejects_duplicate_registration() -> None:
    bus = CommandBus()
    bus.register(AddPoints, AddPointsHandler())

    with pytest.raises(HandlerAlreadyRegisteredError):
        bus.register(AddPoints, AddPointsHandler())


def test_can_replace_registered_handler() -> None:
    bus = CommandBus()
    bus.register(AddPoints, AddPointsHandler())
    replacement = AddPointsHandler()

    bus.register(AddPoints, replacement, replace=True)

    assert bus.dispatch(AddPoints(user_id="u-1", amount=3)) == 3


def test_raises_for_missing_handler() -> None:
    with pytest.raises(HandlerNotFoundError):
        CommandBus().dispatch(AddPoints(user_id="u-1", amount=1))


def test_unregister_returns_state() -> None:
    bus = CommandBus()
    bus.register(AddPoints, AddPointsHandler())

    assert bus.unregister(AddPoints) is True
    assert bus.unregister(AddPoints) is False
    assert bus.has_handler(AddPoints) is False


def test_rejects_invalid_handler() -> None:
    with pytest.raises(InvalidHandlerError):
        CommandBus().register(AddPoints, object())  # type: ignore[arg-type]


def test_middleware_runs_in_registration_order() -> None:
    events: list[str] = []

    def first(command: Command, next_handler):
        events.append("first:before")
        result = next_handler(command)
        events.append("first:after")
        return result

    def second(command: Command, next_handler):
        events.append("second:before")
        result = next_handler(command)
        events.append("second:after")
        return result

    bus = CommandBus([first, second])
    bus.register(AddPoints, AddPointsHandler())

    assert bus.dispatch(AddPoints(user_id="u-1", amount=2)) == 2
    assert events == [
        "first:before",
        "second:before",
        "second:after",
        "first:after",
    ]


def test_command_metadata_is_generated() -> None:
    command = AddPoints(user_id="u-1", amount=1)

    assert command.command_id is not None
    assert command.created_at.tzinfo is not None
