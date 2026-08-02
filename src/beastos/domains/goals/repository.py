from __future__ import annotations

from abc import ABC, abstractmethod
from threading import RLock
from uuid import UUID

from .models import Goal, GoalStatus


class GoalRepository(ABC):
    @abstractmethod
    def save(self, goal: Goal) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, goal_id: UUID) -> Goal | None:
        raise NotImplementedError

    @abstractmethod
    def list(self, *, status: GoalStatus | None = None) -> list[Goal]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, goal_id: UUID) -> bool:
        raise NotImplementedError


class InMemoryGoalRepository(GoalRepository):
    def __init__(self) -> None:
        self._items: dict[UUID, Goal] = {}
        self._lock = RLock()

    def save(self, goal: Goal) -> None:
        with self._lock:
            self._items[goal.id] = goal

    def get(self, goal_id: UUID) -> Goal | None:
        with self._lock:
            return self._items.get(goal_id)

    def list(self, *, status: GoalStatus | None = None) -> list[Goal]:
        with self._lock:
            values = list(self._items.values())
        if status is not None:
            values = [goal for goal in values if goal.status is status]
        return sorted(values, key=lambda goal: goal.created_at)

    def delete(self, goal_id: UUID) -> bool:
        with self._lock:
            return self._items.pop(goal_id, None) is not None
