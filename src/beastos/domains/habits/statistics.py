from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from .models import Habit
from .streaks import current_streak, longest_streak


@dataclass(frozen=True, slots=True)
class HabitStatistics:
    completions: int
    current_streak: int
    longest_streak: int
    completion_rate: float


def calculate_statistics(
    habit: Habit,
    *,
    since: date,
    until: date,
) -> HabitStatistics:
    if until < since:
        raise ValueError("until must be on or after since")

    relevant = {
        value for value in habit.completed_dates
        if since <= value <= until
    }
    total_days = (until - since).days + 1
    rate = round((len(relevant) / total_days) * 100, 2)

    return HabitStatistics(
        completions=len(relevant),
        current_streak=current_streak(habit.completed_dates, today=until),
        longest_streak=longest_streak(habit.completed_dates),
        completion_rate=rate,
    )
