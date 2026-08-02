from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from .exceptions import (
    DuplicateHabitCompletionError,
    InvalidHabitTransitionError,
)


class HabitFrequency(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


class HabitStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class Habit:
    id: UUID
    name: str
    description: str
    frequency: HabitFrequency
    status: HabitStatus
    target_per_period: int
    completed_dates: frozenset[date]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        *,
        name: str,
        description: str = "",
        frequency: HabitFrequency = HabitFrequency.DAILY,
        target_per_period: int = 1,
    ) -> "Habit":
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("name must not be empty")
        if target_per_period <= 0:
            raise ValueError("target_per_period must be positive")
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            name=clean_name,
            description=description.strip(),
            frequency=frequency,
            status=HabitStatus.ACTIVE,
            target_per_period=target_per_period,
            completed_dates=frozenset(),
            created_at=now,
            updated_at=now,
        )

    def complete_on(self, completion_date: date) -> "Habit":
        if self.status is not HabitStatus.ACTIVE:
            raise InvalidHabitTransitionError(
                "only active habits can be completed"
            )
        if completion_date in self.completed_dates:
            raise DuplicateHabitCompletionError(
                f"habit already completed on {completion_date.isoformat()}"
            )
        return replace(
            self,
            completed_dates=self.completed_dates | {completion_date},
            updated_at=datetime.now(timezone.utc),
        )

    def pause(self) -> "Habit":
        if self.status is not HabitStatus.ACTIVE:
            raise InvalidHabitTransitionError("habit is not active")
        return replace(
            self,
            status=HabitStatus.PAUSED,
            updated_at=datetime.now(timezone.utc),
        )

    def resume(self) -> "Habit":
        if self.status is not HabitStatus.PAUSED:
            raise InvalidHabitTransitionError("habit is not paused")
        return replace(
            self,
            status=HabitStatus.ACTIVE,
            updated_at=datetime.now(timezone.utc),
        )

    def archive(self) -> "Habit":
        if self.status is HabitStatus.ARCHIVED:
            raise InvalidHabitTransitionError("habit is already archived")
        return replace(
            self,
            status=HabitStatus.ARCHIVED,
            updated_at=datetime.now(timezone.utc),
        )
