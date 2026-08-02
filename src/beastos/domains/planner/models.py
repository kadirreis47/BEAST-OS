from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import date, datetime, time, timedelta, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from .exceptions import InvalidTimeBlockError


class BlockType(StrEnum):
    FOCUS = "focus"
    TASK = "task"
    BREAK = "break"
    HABIT = "habit"
    GOAL = "goal"


class RecurrenceType(StrEnum):
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass(frozen=True, slots=True)
class RecurrenceRule:
    type: RecurrenceType = RecurrenceType.NONE
    interval: int = 1
    until: date | None = None

    def __post_init__(self) -> None:
        if self.interval <= 0:
            raise ValueError("recurrence interval must be positive")


@dataclass(frozen=True, slots=True)
class TimeBlock:
    id: UUID
    title: str
    start: datetime
    end: datetime
    type: BlockType = BlockType.TASK
    completed: bool = False
    notes: str = ""
    recurrence: RecurrenceRule = field(default_factory=RecurrenceRule)
    source_id: UUID | None = None
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @classmethod
    def create(
        cls,
        *,
        title: str,
        start: datetime,
        end: datetime,
        type: BlockType = BlockType.TASK,
        notes: str = "",
        recurrence: RecurrenceRule | None = None,
        source_id: UUID | None = None,
    ) -> "TimeBlock":
        clean_title = title.strip()
        if not clean_title:
            raise InvalidTimeBlockError("title must not be empty")
        if start.tzinfo is None or end.tzinfo is None:
            raise InvalidTimeBlockError("start and end must be timezone-aware")
        if end <= start:
            raise InvalidTimeBlockError("end must be after start")
        now = datetime.now(timezone.utc)
        return cls(
            id=uuid4(),
            title=clean_title,
            start=start,
            end=end,
            type=type,
            notes=notes.strip(),
            recurrence=recurrence or RecurrenceRule(),
            source_id=source_id,
            created_at=now,
            updated_at=now,
        )

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)

    def overlaps(self, other: "TimeBlock") -> bool:
        return self.start < other.end and other.start < self.end

    def complete(self) -> "TimeBlock":
        if self.completed:
            return self
        return replace(
            self,
            completed=True,
            updated_at=datetime.now(timezone.utc),
        )

    def clone_for(self, target_date: date) -> "TimeBlock":
        start = datetime.combine(
            target_date,
            self.start.timetz(),
        )
        end_date = target_date
        if self.end.date() > self.start.date():
            end_date += timedelta(days=1)
        end = datetime.combine(end_date, self.end.timetz())
        return TimeBlock.create(
            title=self.title,
            start=start,
            end=end,
            type=self.type,
            notes=self.notes,
            recurrence=self.recurrence,
            source_id=self.id,
        )


@dataclass(frozen=True, slots=True)
class PlannerDay:
    day: date
    blocks: tuple[TimeBlock, ...] = ()

    @property
    def score(self) -> float:
        if not self.blocks:
            return 0.0
        completed = sum(block.completed for block in self.blocks)
        return round((completed / len(self.blocks)) * 100, 2)

    @property
    def total_focus_minutes(self) -> int:
        return sum(
            block.duration_minutes
            for block in self.blocks
            if block.type is BlockType.FOCUS
        )

    def with_block(self, block: TimeBlock) -> "PlannerDay":
        return replace(
            self,
            blocks=tuple(sorted(
                (*self.blocks, block),
                key=lambda item: item.start,
            )),
        )

    def replace_block(self, block: TimeBlock) -> "PlannerDay":
        replaced = tuple(
            block if item.id == block.id else item
            for item in self.blocks
        )
        return replace(self, blocks=replaced)

    def without_block(self, block_id: UUID) -> "PlannerDay":
        return replace(
            self,
            blocks=tuple(
                item for item in self.blocks if item.id != block_id
            ),
        )
