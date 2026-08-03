from beastos.analytics.insights import generate
from beastos.analytics.scores import AnalyticsSnapshot
from beastos.presentation.dashboard import DashboardBuilder
from beastos.presentation.dashboard.models import DashboardTrendDirection
from beastos.presentation.dashboard.serializer import dashboard_to_dict


def make_snapshot() -> AnalyticsSnapshot:
    return AnalyticsSnapshot(
        goals_completed=4,
        goals_total=5,
        habits_completed=6,
        habits_target=8,
        planner_completion=80,
        focus_minutes=240,
    )


def test_dashboard_builder_creates_cards():
    snapshot = make_snapshot()
    state = DashboardBuilder().build(
        snapshot,
        insights=generate(snapshot),
        previous_productivity=60,
    )

    assert state.score == snapshot.productivity
    assert len(state.cards) == 5
    assert state.get_card("goals").progress == 80.0
    assert state.get_card("habits").progress == 75.0
    assert state.get_card("productivity").trend.direction is DashboardTrendDirection.UP


def test_dashboard_state_serialization():
    state = DashboardBuilder().build(make_snapshot())
    payload = dashboard_to_dict(state)

    assert payload["score"] == state.score
    assert payload["cards"][0]["key"] == "productivity"
    assert isinstance(payload["generated_at_iso"], str)


def test_dashboard_card_lookup_rejects_missing_key():
    state = DashboardBuilder().build(make_snapshot())

    try:
        state.get_card("missing")
    except KeyError as exc:
        assert exc.args == ("missing",)
    else:
        raise AssertionError("expected KeyError")
