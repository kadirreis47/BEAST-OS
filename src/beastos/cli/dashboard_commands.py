from __future__ import annotations

from beastos.application import bootstrap_application
from beastos.presentation.dashboard import DashboardBuilder
from beastos.analytics.scores import AnalyticsSnapshot


def register_dashboard_commands(subparsers) -> None:
    dashboard = subparsers.add_parser(
        "dashboard",
        help="Show the latest dashboard snapshot",
    )
    dashboard.set_defaults(handler=_show_dashboard)


def _show_dashboard(_args) -> int:
    application = bootstrap_application()
    record = application.dashboard_repository.latest()

    if record is None:
        print("No dashboard snapshot found.")
        return 0

    analytics = AnalyticsSnapshot(
        goals_completed=record.goals_completed,
        goals_total=record.goals_total,
        habits_completed=record.habits_completed,
        habits_target=record.habits_target,
        planner_completion=record.planner_completion,
        focus_minutes=record.focus_minutes,
    )
    state = DashboardBuilder().build(analytics)

    print("=== BEAST OS ===")
    print(f"Productivity: {state.score}%")
    for card in state.cards:
        suffix = card.unit or ""
        print(f"{card.title}: {card.value}{suffix}")

    return 0
