from __future__ import annotations

from collections.abc import Callable
from datetime import date
from uuid import UUID

from .events import HabitCompleted, HabitCreated, HabitEvent, HabitStreakChanged
from .exceptions import HabitNotFoundError
from .models import Habit, HabitFrequency, HabitStatus
from .repository import HabitRepository
from .streaks import current_streak

EventPublisher = Callable[[HabitEvent], None]


class HabitService:
    def __init__(
        self,
        repository: HabitRepository,
        publisher: EventPublisher | None = None,
    ) -> None:
        self._repository = repository
        self._publisher = publisher or (lambda _: None)

    def create_habit(
        self,
        *,
        name: str,
        description: str = "",
        frequency: HabitFrequency = HabitFrequency.DAILY,
        target_per_period: int = 1,
    ) -> Habit:
        habit = Habit.create(
            name=name,
            description=description,
            frequency=frequency,
            target_per_period=target_per_period,
        )
        self._repository.save(habit)
        self._publisher(HabitCreated(habit_id=habit.id, name=habit.name))
        return habit

    def get_habit(self, habit_id: UUID) -> Habit:
        habit = self._repository.get(habit_id)
        if habit is None:
            raise HabitNotFoundError(str(habit_id))
        return habit

    def complete(self, habit_id: UUID, completion_date: date | None = None) -> Habit:
        value = completion_date or date.today()
        habit = self.get_habit(habit_id)
        previous_streak = current_streak(habit.completed_dates, today=value)
        updated = habit.complete_on(value)
        new_streak = current_streak(updated.completed_dates, today=value)
        self._repository.save(updated)
        self._publisher(
            HabitCompleted(habit_id=habit_id, completion_date=value)
        )
        if previous_streak != new_streak:
            self._publisher(
                HabitStreakChanged(
                    habit_id=habit_id,
                    previous=previous_streak,
                    current=new_streak,
                )
            )
        return updated

    def pause(self, habit_id: UUID) -> Habit:
        updated = self.get_habit(habit_id).pause()
        self._repository.save(updated)
        return updated

    def resume(self, habit_id: UUID) -> Habit:
        updated = self.get_habit(habit_id).resume()
        self._repository.save(updated)
        return updated

    def archive(self, habit_id: UUID) -> Habit:
        updated = self.get_habit(habit_id).archive()
        self._repository.save(updated)
        return updated

    def list_habits(self, *, status: HabitStatus | None = None) -> list[Habit]:
        return self._repository.list(status=status)
