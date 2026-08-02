from __future__ import annotations

from abc import ABC, abstractmethod
from threading import RLock
from uuid import UUID

from .models import Habit, HabitStatus


class HabitRepository(ABC):
    @abstractmethod
    def save(self, habit: Habit) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, habit_id: UUID) -> Habit | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, *, status: HabitStatus | None = None) -> list[Habit]:
        raise NotImplementedError


class InMemoryHabitRepository(HabitRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, Habit] = {}
        self._lock = RLock()

    def save(self, habit: Habit) -> None:
        with self._lock:
            self._items[habit.id] = habit

    def get(self, habit_id: UUID) -> Habit | None:
        with self._lock:
            return self._items.get(habit_id)

    def list(self, *, status: HabitStatus | None = None) -> list[Habit]:
        with self._lock:
            items = list(self._items.values())
        if status is not None:
            items = [habit for habit in items if habit.status is status]
        return sorted(items, key=lambda habit: habit.created_at)
