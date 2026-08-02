from __future__ import annotations

from datetime import date, timedelta

from .models import RecurrenceType, TimeBlock


def expand_recurrence(
    block: TimeBlock,
    *,
    range_start: date,
    range_end: date,
) -> list[TimeBlock]:
    if range_end < range_start:
        raise ValueError("range_end must be on or after range_start")

    rule = block.recurrence
    if rule.type is RecurrenceType.NONE:
        return [block] if range_start <= block.start.date() <= range_end else []

    step = (
        timedelta(days=rule.interval)
        if rule.type is RecurrenceType.DAILY
        else timedelta(weeks=rule.interval)
    )

    results: list[TimeBlock] = []
    current = block.start.date()
    hard_end = min(range_end, rule.until) if rule.until else range_end

    while current <= hard_end:
        if current >= range_start:
            results.append(
                block if current == block.start.date()
                else block.clone_for(current)
            )
        current += step

    return results
