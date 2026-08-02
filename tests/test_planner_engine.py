from datetime import date, datetime, timedelta, timezone

import pytest

from beastos.domains.planner.events import (
    PlannerBlockAdded,
    PlannerBlockCompleted,
    PlannerBlockRemoved,
)
from beastos.domains.planner.exceptions import TimeBlockConflictError
from beastos.domains.planner.models import (
    BlockType,
    RecurrenceRule,
    RecurrenceType,
    TimeBlock,
)
from beastos.domains.planner.recurrence import expand_recurrence
from beastos.domains.planner.repository import InMemoryPlannerRepository
from beastos.domains.planner.service import PlannerService
from beastos.domains.planner.statistics import calculate_planner_statistics


UTC = timezone.utc


def make_block(
    *,
    title: str = "Deep Work",
    start_hour: int = 9,
    end_hour: int = 10,
    day: date | None = None,
    completed: bool = False,
    type: BlockType = BlockType.FOCUS,
    recurrence: RecurrenceRule | None = None,
) -> TimeBlock:
    value = day or date.today()
    block = TimeBlock.create(
        title=title,
        start=datetime(value.year, value.month, value.day, start_hour, tzinfo=UTC),
        end=datetime(value.year, value.month, value.day, end_hour, tzinfo=UTC),
        type=type,
        recurrence=recurrence,
    )
    return block.complete() if completed else block


def test_add_complete_remove_block_and_events():
    events = []
    service = PlannerService(InMemoryPlannerRepository(), events.append)
    block = make_block()

    planner_day = service.add_block(block)
    assert planner_day.blocks == (block,)
    assert isinstance(events[-1], PlannerBlockAdded)

    planner_day = service.complete_block(planner_day.day, block.id)
    assert planner_day.blocks[0].completed is True
    assert isinstance(events[-1], PlannerBlockCompleted)

    planner_day = service.remove_block(planner_day.day, block.id)
    assert planner_day.blocks == ()
    assert isinstance(events[-1], PlannerBlockRemoved)


def test_conflicting_blocks_are_rejected():
    service = PlannerService(InMemoryPlannerRepository())
    service.add_block(make_block(start_hour=9, end_hour=11))

    with pytest.raises(TimeBlockConflictError):
        service.add_block(make_block(start_hour=10, end_hour=12))


def test_touching_blocks_do_not_conflict():
    service = PlannerService(InMemoryPlannerRepository())
    service.add_block(make_block(start_hour=9, end_hour=10))
    planner_day = service.add_block(
        make_block(title="Email", start_hour=10, end_hour=11)
    )

    assert len(planner_day.blocks) == 2


def test_daily_recurrence_expansion():
    today = date.today()
    block = make_block(
        day=today,
        recurrence=RecurrenceRule(
            type=RecurrenceType.DAILY,
            interval=1,
            until=today + timedelta(days=2),
        ),
    )

    occurrences = expand_recurrence(
        block,
        range_start=today,
        range_end=today + timedelta(days=5),
    )

    assert len(occurrences) == 3
    assert [item.start.date() for item in occurrences] == [
        today,
        today + timedelta(days=1),
        today + timedelta(days=2),
    ]


def test_planner_statistics():
    service = PlannerService(InMemoryPlannerRepository())
    first = make_block(completed=True)
    second = make_block(
        title="Task",
        start_hour=10,
        end_hour=11,
        type=BlockType.TASK,
    )
    service.add_block(first)
    service.add_block(second)

    stats = calculate_planner_statistics(
        service.list_days(date.today(), date.today())
    )

    assert stats.total_blocks == 2
    assert stats.completed_blocks == 1
    assert stats.completion_rate == 50.0
    assert stats.focus_minutes == 60
    assert stats.planned_minutes == 120


def test_planner_day_score_and_focus_minutes():
    service = PlannerService(InMemoryPlannerRepository())
    day = service.add_block(make_block(completed=True))
    day = service.add_block(
        make_block(
            title="Break",
            start_hour=10,
            end_hour=11,
            type=BlockType.BREAK,
        )
    )

    assert day.score == 50.0
    assert day.total_focus_minutes == 60
