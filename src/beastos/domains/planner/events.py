from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class PlannerEvent:
    planner_day: date
    block_id: UUID
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(frozen=True, slots=True)
class PlannerBlockAdded(PlannerEvent):
    title: str = ""


@dataclass(frozen=True, slots=True)
class PlannerBlockCompleted(PlannerEvent):
    pass


@dataclass(frozen=True, slots=True)
class PlannerBlockRemoved(PlannerEvent):
    pass
