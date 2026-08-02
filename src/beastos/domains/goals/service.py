from __future__ import annotations

from collections.abc import Callable
from datetime import date
from uuid import UUID

from .events import (
    GoalArchived,
    GoalCompleted,
    GoalCreated,
    GoalEvent,
    GoalProgressChanged,
)
from .exceptions import GoalNotFoundError
from .models import Goal, GoalPriority, GoalStatus
from .repository import GoalRepository

EventPublisher = Callable[[GoalEvent], None]


class GoalService:
    def __init__(
        self,
        repository: GoalRepository,
        publisher: EventPublisher | None = None,
    ) -> None:
        self._repository = repository
        self._publisher = publisher or (lambda _: None)

    def create_goal(
        self,
        *,
        title: str,
        description: str = "",
        priority: GoalPriority = GoalPriority.MEDIUM,
        target_date: date | None = None,
        activate: bool = True,
    ) -> Goal:
        goal = Goal.create(
            title=title,
            description=description,
            priority=priority,
            target_date=target_date,
        )
        if activate:
            goal = goal.transition_to(GoalStatus.ACTIVE)
        self._repository.save(goal)
        self._publisher(GoalCreated(goal_id=goal.id, title=goal.title))
        return goal

    def get_goal(self, goal_id: UUID) -> Goal:
        goal = self._repository.get(goal_id)
        if goal is None:
            raise GoalNotFoundError(str(goal_id))
        return goal

    def update_progress(self, goal_id: UUID, value: int) -> Goal:
        goal = self.get_goal(goal_id)
        previous = goal.progress
        updated = goal.update_progress(value)
        self._repository.save(updated)
        self._publisher(
            GoalProgressChanged(
                goal_id=goal_id,
                previous=previous,
                current=updated.progress,
            )
        )
        if updated.status is GoalStatus.COMPLETED:
            self._publisher(GoalCompleted(goal_id=goal_id))
        return updated

    def pause(self, goal_id: UUID) -> Goal:
        return self._transition(goal_id, GoalStatus.PAUSED)

    def resume(self, goal_id: UUID) -> Goal:
        return self._transition(goal_id, GoalStatus.ACTIVE)

    def complete(self, goal_id: UUID) -> Goal:
        updated = self._transition(goal_id, GoalStatus.COMPLETED)
        self._publisher(GoalCompleted(goal_id=goal_id))
        return updated

    def archive(self, goal_id: UUID) -> Goal:
        updated = self._transition(goal_id, GoalStatus.ARCHIVED)
        self._publisher(GoalArchived(goal_id=goal_id))
        return updated

    def list_goals(self, *, status: GoalStatus | None = None) -> list[Goal]:
        return self._repository.list(status=status)

    def _transition(self, goal_id: UUID, status: GoalStatus) -> Goal:
        updated = self.get_goal(goal_id).transition_to(status)
        self._repository.save(updated)
        return updated
