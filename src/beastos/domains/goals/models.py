from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from .exceptions import InvalidGoalProgressError, InvalidGoalTransitionError


class GoalStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class GoalPriority(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


_ALLOWED_TRANSITIONS: dict[GoalStatus, set[GoalStatus]] = {
    GoalStatus.DRAFT: {GoalStatus.ACTIVE, GoalStatus.ARCHIVED},
    GoalStatus.ACTIVE: {
        GoalStatus.PAUSED,
        GoalStatus.COMPLETED,
        GoalStatus.ARCHIVED,
    },
    GoalStatus.PAUSED: {GoalStatus.ACTIVE, GoalStatus.ARCHIVED},
    GoalStatus.COMPLETED: {GoalStatus.ARCHIVED},
    GoalStatus.ARCHIVED: set(),
}


@dataclass(frozen=True, slots=True)
class Goal:
    id: UUID
    title: str
    description: str
    priority: GoalPriority
    status: GoalStatus
    progress: int
    target_date: date | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        title: str,
        description: str = "",
        priority: GoalPriority = GoalPriority.MEDIUM,
        target_date: date | None = None,
    ) -> "Goal":
        clean_title = title.strip()
        if not clean_title:
            raise ValueError("title must not be empty")
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            title=clean_title,
            description=description.strip(),
            priority=priority,
            status=GoalStatus.DRAFT,
            progress=0,
            target_date=target_date,
            created_at=now,
            updated_at=now,
        )

    @property
    def is_overdue(self) -> bool:
        return (
            self.target_date is not None
            and self.target_date < date.today()
            and self.status not in {GoalStatus.COMPLETED, GoalStatus.ARCHIVED}
        )

    def transition_to(self, new_status: GoalStatus) -> "Goal":
        if new_status not in _ALLOWED_TRANSITIONS[self.status]:
            raise InvalidGoalTransitionError(
                f"cannot transition goal from {self.status} to {new_status}"
            )
        now = datetime.now(timezone.utc)
        completed_at = now if new_status is GoalStatus.COMPLETED else self.completed_at
        progress = 100 if new_status is GoalStatus.COMPLETED else self.progress
        return replace(
            self,
            status=new_status,
            progress=progress,
            completed_at=completed_at,
            updated_at=now,
        )

    def update_progress(self, value: int) -> "Goal":
        if not 0 <= value <= 100:
            raise InvalidGoalProgressError("progress must be between 0 and 100")
        if self.status not in {GoalStatus.ACTIVE, GoalStatus.PAUSED}:
            raise InvalidGoalTransitionError(
                "progress can only be changed for active or paused goals"
            )
        now = datetime.now(timezone.utc)
        if value == 100:
            return replace(
                self,
                progress=100,
                status=GoalStatus.COMPLETED,
                completed_at=now,
                updated_at=now,
            )
        return replace(self, progress=value, updated_at=now)
