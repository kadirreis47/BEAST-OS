from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class GoalEvent:
    goal_id: UUID
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(frozen=True, slots=True)
class GoalCreated(GoalEvent):
    title: str = ""


@dataclass(frozen=True, slots=True)
class GoalProgressChanged(GoalEvent):
    previous: int = 0
    current: int = 0


@dataclass(frozen=True, slots=True)
class GoalCompleted(GoalEvent):
    pass


@dataclass(frozen=True, slots=True)
class GoalArchived(GoalEvent):
    pass
