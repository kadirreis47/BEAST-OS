from __future__ import annotations

from collections.abc import Callable
from datetime import date
from uuid import UUID

from .conflicts import find_conflicts
from .events import (
    PlannerBlockAdded,
    PlannerBlockCompleted,
    PlannerBlockRemoved,
    PlannerEvent,
)
from .exceptions import (
    PlannerDayNotFoundError,
    TimeBlockConflictError,
    TimeBlockNotFoundError,
)
from .models import PlannerDay, TimeBlock
from .repository import PlannerRepository

EventPublisher = Callable[[PlannerEvent], None]


class PlannerService:
    def __init__(
        self,
        repository: PlannerRepository,
        publisher: EventPublisher | None = None,
    ) -> None:
        self._repository = repository
        self._publisher = publisher or (lambda _: None)

    def get_or_create_day(self, day: date) -> PlannerDay:
        existing = self._repository.get(day)
        if existing is not None:
            return existing
        created = PlannerDay(day=day)
        self._repository.save(created)
        return created

    def get_day(self, day: date) -> PlannerDay:
        planner_day = self._repository.get(day)
        if planner_day is None:
            raise PlannerDayNotFoundError(day.isoformat())
        return planner_day

    def add_block(self, block: TimeBlock) -> PlannerDay:
        planner_day = self.get_or_create_day(block.start.date())
        conflicts = find_conflicts(block, planner_day.blocks)
        if conflicts:
            raise TimeBlockConflictError(
                f"block conflicts with {len(conflicts)} existing block(s)"
            )

        updated = planner_day.with_block(block)
        self._repository.save(updated)
        self._publisher(
            PlannerBlockAdded(
                planner_day=updated.day,
                block_id=block.id,
                title=block.title,
            )
        )
        return updated

    def complete_block(self, day: date, block_id: UUID) -> PlannerDay:
        planner_day = self.get_day(day)
        block = self._find_block(planner_day, block_id)
        completed = block.complete()
        updated = planner_day.replace_block(completed)
        self._repository.save(updated)
        self._publisher(
            PlannerBlockCompleted(
                planner_day=day,
                block_id=block_id,
            )
        )
        return updated

    def remove_block(self, day: date, block_id: UUID) -> PlannerDay:
        planner_day = self.get_day(day)
        self._find_block(planner_day, block_id)
        updated = planner_day.without_block(block_id)
        self._repository.save(updated)
        self._publisher(
            PlannerBlockRemoved(
                planner_day=day,
                block_id=block_id,
            )
        )
        return updated

    def list_days(self, start: date, end: date) -> list[PlannerDay]:
        return self._repository.list_range(start, end)

    @staticmethod
    def _find_block(planner_day: PlannerDay, block_id: UUID) -> TimeBlock:
        for block in planner_day.blocks:
            if block.id == block_id:
                return block
        raise TimeBlockNotFoundError(str(block_id))
