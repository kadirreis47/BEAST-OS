from datetime import date, timedelta

import pytest

from beastos.domains.habits.events import (
    HabitCompleted,
    HabitCreated,
    HabitStreakChanged,
)
from beastos.domains.habits.exceptions import DuplicateHabitCompletionError
from beastos.domains.habits.models import HabitStatus
from beastos.domains.habits.repository import InMemoryHabitRepository
from beastos.domains.habits.service import HabitService
from beastos.domains.habits.statistics import calculate_statistics
from beastos.domains.habits.streaks import current_streak, longest_streak


def test_habit_creation_and_completion_events():
    events = []
    service = HabitService(InMemoryHabitRepository(), events.append)
    today = date.today()

    habit = service.create_habit(name="Read 20 pages")
    completed = service.complete(habit.id, today)

    assert today in completed.completed_dates
    assert isinstance(events[0], HabitCreated)
    assert any(isinstance(event, HabitCompleted) for event in events)
    assert any(isinstance(event, HabitStreakChanged) for event in events)


def test_duplicate_completion_rejected():
    service = HabitService(InMemoryHabitRepository())
    habit = service.create_habit(name="Meditate")
    today = date.today()
    service.complete(habit.id, today)

    with pytest.raises(DuplicateHabitCompletionError):
        service.complete(habit.id, today)


def test_pause_resume_archive():
    service = HabitService(InMemoryHabitRepository())
    habit = service.create_habit(name="Exercise")

    paused = service.pause(habit.id)
    assert paused.status is HabitStatus.PAUSED

    resumed = service.resume(habit.id)
    assert resumed.status is HabitStatus.ACTIVE

    archived = service.archive(habit.id)
    assert archived.status is HabitStatus.ARCHIVED


def test_streak_calculations():
    today = date.today()
    values = {
        today,
        today - timedelta(days=1),
        today - timedelta(days=2),
        today - timedelta(days=5),
    }

    assert current_streak(values, today=today) == 3
    assert longest_streak(values) == 3


def test_habit_statistics():
    service = HabitService(InMemoryHabitRepository())
    habit = service.create_habit(name="Journal")
    today = date.today()
    for offset in (0, 1, 2):
        habit = service.complete(habit.id, today - timedelta(days=offset))

    stats = calculate_statistics(
        habit,
        since=today - timedelta(days=6),
        until=today,
    )

    assert stats.completions == 3
    assert stats.current_streak == 3
    assert stats.longest_streak == 3
    assert stats.completion_rate == 42.86


def test_status_filtering():
    service = HabitService(InMemoryHabitRepository())
    active = service.create_habit(name="Active")
    archived = service.create_habit(name="Archived")
    service.archive(archived.id)

    result = service.list_habits(status=HabitStatus.ACTIVE)

    assert [habit.id for habit in result] == [active.id]
