from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any


class TaskStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    DISABLED = "disabled"


@dataclass(frozen=True, slots=True)
class IntervalSchedule:
    seconds: int

    def __post_init__(self) -> None:
        if self.seconds < 1:
            raise ValueError("seconds must be at least 1")

    def next_run(self, after: datetime) -> datetime:
        if after.tzinfo is None:
            raise ValueError("after must be timezone-aware")
        return after + timedelta(seconds=self.seconds)


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: int = 30
    multiplier: float = 2.0
    max_delay_seconds: int = 3600

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.base_delay_seconds < 0:
            raise ValueError("base_delay_seconds cannot be negative")
        if self.multiplier < 1:
            raise ValueError("multiplier must be at least 1")
        if self.max_delay_seconds < self.base_delay_seconds:
            raise ValueError("max_delay_seconds cannot be below base delay")

    def delay_for(self, failed_attempt: int) -> int:
        if failed_attempt < 1:
            raise ValueError("failed_attempt must be at least 1")
        delay = self.base_delay_seconds * (self.multiplier ** (failed_attempt - 1))
        return min(round(delay), self.max_delay_seconds)


@dataclass(slots=True)
class ScheduledTask:
    task_id: str
    handler_name: str
    schedule: IntervalSchedule
    payload: dict[str, Any] = field(default_factory=dict)
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    enabled: bool = True
    status: TaskStatus = TaskStatus.PENDING
    attempts: int = 0
    next_run_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_run_at: datetime | None = None
    last_error: str | None = None

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError("task_id cannot be empty")
        if not self.handler_name.strip():
            raise ValueError("handler_name cannot be empty")
        if self.next_run_at.tzinfo is None:
            raise ValueError("next_run_at must be timezone-aware")
