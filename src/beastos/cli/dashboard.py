from beastos.analytics.scores import AnalyticsSnapshot
from beastos.analytics.insights import generate
from beastos.presentation.dashboard.builder import DashboardBuilder

def render_demo():
    snap=AnalyticsSnapshot(
        goals_completed=3,
        goals_total=5,
        habits_completed=6,
        habits_target=8,
        planner_completion=82,
        focus_minutes=210,
    )
    state=DashboardBuilder().build(snap,insights=generate(snap))
    print("=== BEAST OS ===")
    print(f"Score : {state.score}%")
    for c in state.cards:
        print(f"{c.title}: {c.value}{c.unit or ''}")
