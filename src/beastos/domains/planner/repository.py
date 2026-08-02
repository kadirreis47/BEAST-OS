from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from threading import RLock

from .models import PlannerDay


class PlannerRepository(ABC):
    @abstractmethod
    def save(self, planner_day: PlannerDay) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, day: date) -> PlannerDay | None:
        raise NotImplementedError

    @abstractmethod
    def list_range(self, start: date, end: date) -> list[PlannerDay]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, day: date) -> bool:
        raise NotImplementedError


class InMemoryPlannerRepository(PlannerRepository):
    def __init__(self) -> None:
        self._items: dict[date, PlannerDay] = {}
        self._lock = RLock()

    def save(self, planner_day: PlannerDay) -> None:
        with self._lock:
            self._items[planner_day.day] = planner_day

    def get(self, day: date) -> PlannerDay | None:
        with self._lock:
            return self._items.get(day)

    def list_range(self, start: date, end: date) -> list[PlannerDay]:
        if end < start:
            raise ValueError("end must be on or after start")
        with self._lock:
            values = [
                item
                for key, item in self._items.items()
                if start <= key <= end
            ]
        return sorted(values, key=lambda item: item.day)

    def delete(self, day: date) -> bool:
        with self._lock:
            return self._items.pop(day, None) is not None
