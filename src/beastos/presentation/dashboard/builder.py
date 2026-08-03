from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

from .models import DashboardCard, DashboardState, DashboardTrend


class AnalyticsLike(Protocol):
    goals_completed: int
    goals_total: int
    habits_completed: int
    habits_target: int
    planner_completion: float
    focus_minutes: int

    @property
    def goal_score(self) -> float: ...

    @property
    def habit_score(self) -> float: ...

    @property
    def focus_score(self) -> float: ...

    @property
    def productivity(self) -> float: ...


class DashboardBuilder:
    def build(
        self,
        snapshot: AnalyticsLike,
        *,
        insights: list[str] | tuple[str, ...] = (),
        previous_productivity: float | None = None,
    ) -> DashboardState:
        trend = (
            DashboardTrend.from_values(
                current=snapshot.productivity,
                previous=previous_productivity,
            )
            if previous_productivity is not None
            else None
        )

        cards = (
            DashboardCard(
                key="productivity",
                title="Productivity",
                value=snapshot.productivity,
                unit="%",
                progress=snapshot.productivity,
                trend=trend,
            ),
            DashboardCard(
                key="goals",
                title="Goals",
                value=f"{snapshot.goals_completed}/{snapshot.goals_total}",
                progress=snapshot.goal_score,
                metadata={
                    "completed": snapshot.goals_completed,
                    "total": snapshot.goals_total,
                },
            ),
            DashboardCard(
                key="habits",
                title="Habits",
                value=f"{snapshot.habits_completed}/{snapshot.habits_target}",
                progress=snapshot.habit_score,
                metadata={
                    "completed": snapshot.habits_completed,
                    "target": snapshot.habits_target,
                },
            ),
            DashboardCard(
                key="planner",
                title="Planner",
                value=snapshot.planner_completion,
                unit="%",
                progress=snapshot.planner_completion,
            ),
            DashboardCard(
                key="focus",
                title="Focus",
                value=snapshot.focus_minutes,
                unit="min",
                progress=snapshot.focus_score,
            ),
        )

        return DashboardState(
            score=snapshot.productivity,
            cards=cards,
            insights=tuple(insights),
            generated_at_iso=datetime.now(timezone.utc).isoformat(),
        )
