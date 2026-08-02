
from beastos.integration.state_projection import LifeState

def test_productivity_score():
    state=LifeState(
        goals_total=5,
        goals_completed=3,
        habits_completed_today=4,
        planner_completion=80,
        focus_minutes=180,
    )
    assert state.productivity_score>0
