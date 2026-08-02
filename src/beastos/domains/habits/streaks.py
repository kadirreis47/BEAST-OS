from __future__ import annotations

from datetime import date, timedelta
from collections.abc import Iterable


def current_streak(completed_dates: Iterable[date], *, today: date | None = None) -> int:
    completed = set(completed_dates)
    cursor = today or date.today()
    if cursor not in completed and (cursor - timedelta(days=1)) in completed:
        cursor -= timedelta(days=1)

    streak = 0
    while cursor in completed:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def longest_streak(completed_dates: Iterable[date]) -> int:
    completed = sorted(set(completed_dates))
    if not completed:
        return 0

    longest = 1
    running = 1
    for previous, current in zip(completed, completed[1:]):
        if current - previous == timedelta(days=1):
            running += 1
            longest = max(longest, running)
        else:
            running = 1
    return longest
