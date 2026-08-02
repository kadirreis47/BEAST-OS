from __future__ import annotations

from dataclasses import dataclass

from .models import Goal, GoalStatus


@dataclass(frozen=True, slots=True)
class GoalStatistics:
    total: int
    active: int
    completed: int
    overdue: int
    completion_rate: float


def calculate_statistics(goals: list[Goal]) -> GoalStatistics:
    total = len(goals)
    completed = sum(goal.status is GoalStatus.COMPLETED for goal in goals)
    active = sum(goal.status is GoalStatus.ACTIVE for goal in goals)
    overdue = sum(goal.is_overdue for goal in goals)
    rate = round((completed / total) * 100, 2) if total else 0.0
    return GoalStatistics(
        total=total,
        active=active,
        completed=completed,
        overdue=overdue,
        completion_rate=rate,
    )
