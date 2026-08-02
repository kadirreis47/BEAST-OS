from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class HabitEvent:
    habit_id: UUID
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(frozen=True, slots=True)
class HabitCreated(HabitEvent):
    name: str = ""


@dataclass(frozen=True, slots=True)
class HabitCompleted(HabitEvent):
    completion_date: date = field(default_factory=date.today)


@dataclass(frozen=True, slots=True)
class HabitStreakChanged(HabitEvent):
    previous: int = 0
    current: int = 0
