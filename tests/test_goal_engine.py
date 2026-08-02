from datetime import date, timedelta

import pytest

from beastos.domains.goals.events import (
    GoalCompleted,
    GoalCreated,
    GoalProgressChanged,
)
from beastos.domains.goals.exceptions import InvalidGoalProgressError
from beastos.domains.goals.models import GoalPriority, GoalStatus
from beastos.domains.goals.repository import InMemoryGoalRepository
from beastos.domains.goals.service import GoalService
from beastos.domains.goals.statistics import calculate_statistics


def test_goal_lifecycle_and_events():
    events = []
    service = GoalService(InMemoryGoalRepository(), events.append)

    goal = service.create_goal(
        title="Run a marathon",
        priority=GoalPriority.HIGH,
    )
    assert goal.status is GoalStatus.ACTIVE
    assert isinstance(events[0], GoalCreated)

    goal = service.update_progress(goal.id, 45)
    assert goal.progress == 45
    assert isinstance(events[-1], GoalProgressChanged)

    goal = service.update_progress(goal.id, 100)
    assert goal.status is GoalStatus.COMPLETED
    assert isinstance(events[-1], GoalCompleted)


def test_pause_resume_archive():
    service = GoalService(InMemoryGoalRepository())
    goal = service.create_goal(title="Read 20 books")

    paused = service.pause(goal.id)
    assert paused.status is GoalStatus.PAUSED

    resumed = service.resume(goal.id)
    assert resumed.status is GoalStatus.ACTIVE

    archived = service.archive(goal.id)
    assert archived.status is GoalStatus.ARCHIVED


def test_invalid_progress_rejected():
    service = GoalService(InMemoryGoalRepository())
    goal = service.create_goal(title="Save money")

    with pytest.raises(InvalidGoalProgressError):
        service.update_progress(goal.id, 101)


def test_statistics_include_overdue():
    service = GoalService(InMemoryGoalRepository())
    overdue = service.create_goal(
        title="Old deadline",
        target_date=date.today() - timedelta(days=1),
    )
    completed = service.create_goal(title="Done")
    service.complete(completed.id)

    stats = calculate_statistics(service.list_goals())

    assert stats.total == 2
    assert stats.completed == 1
    assert stats.overdue == 1
    assert stats.completion_rate == 50.0


def test_repository_status_filtering():
    service = GoalService(InMemoryGoalRepository())
    active = service.create_goal(title="Active")
    completed = service.create_goal(title="Completed")
    service.complete(completed.id)

    result = service.list_goals(status=GoalStatus.ACTIVE)

    assert [goal.id for goal in result] == [active.id]
