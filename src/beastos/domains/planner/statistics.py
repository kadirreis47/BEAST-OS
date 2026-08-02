from __future__ import annotations

from dataclasses import dataclass

from .models import BlockType, PlannerDay


@dataclass(frozen=True, slots=True)
class PlannerStatistics:
    total_blocks: int
    completed_blocks: int
    completion_rate: float
    focus_minutes: int
    planned_minutes: int


def calculate_planner_statistics(
    planner_days: list[PlannerDay],
) -> PlannerStatistics:
    blocks = [
        block
        for planner_day in planner_days
        for block in planner_day.blocks
    ]
    total = len(blocks)
    completed = sum(block.completed for block in blocks)
    completion_rate = round((completed / total) * 100, 2) if total else 0.0
    focus_minutes = sum(
        block.duration_minutes
        for block in blocks
        if block.type is BlockType.FOCUS
    )
    planned_minutes = sum(block.duration_minutes for block in blocks)

    return PlannerStatistics(
        total_blocks=total,
        completed_blocks=completed,
        completion_rate=completion_rate,
        focus_minutes=focus_minutes,
        planned_minutes=planned_minutes,
    )
