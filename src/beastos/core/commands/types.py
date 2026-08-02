from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, Protocol, TypeVar, runtime_checkable
from uuid import UUID, uuid4

ResultT = TypeVar("ResultT", covariant=True)
CommandT = TypeVar("CommandT", contravariant=True)


@dataclass(frozen=True, slots=True, kw_only=True)
class Command:
    command_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@runtime_checkable
class CommandHandler(Protocol[CommandT, ResultT]):
    def handle(self, command: CommandT) -> ResultT:
        """Execute a command and return its result."""
