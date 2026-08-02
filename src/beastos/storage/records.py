from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True, slots=True)
class DailyMetric:
    metric_date: date
    key: str
    value: float
    unit: str | None = None
    source: str = "manual"

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("key cannot be empty")
        if not self.source.strip():
            raise ValueError("source cannot be empty")


@dataclass(frozen=True, slots=True)
class HabitLog:
    habit_id: str
    logged_at: datetime
    completed: bool
    value: float | None = None
    note: str | None = None

    def __post_init__(self) -> None:
        if not self.habit_id.strip():
            raise ValueError("habit_id cannot be empty")
        if self.logged_at.tzinfo is None:
            raise ValueError("logged_at must be timezone-aware")
