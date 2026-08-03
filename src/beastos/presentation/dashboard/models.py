from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class DashboardTrendDirection(StrEnum):
    UP = "up"
    DOWN = "down"
    FLAT = "flat"


@dataclass(frozen=True, slots=True)
class DashboardTrend:
    direction: DashboardTrendDirection
    change_percent: float

    @classmethod
    def from_values(
        cls,
        *,
        current: float,
        previous: float,
    ) -> "DashboardTrend":
        if previous == 0:
            change = 100.0 if current > 0 else 0.0
        else:
            change = round(((current - previous) / abs(previous)) * 100, 2)

        if change > 0:
            direction = DashboardTrendDirection.UP
        elif change < 0:
            direction = DashboardTrendDirection.DOWN
        else:
            direction = DashboardTrendDirection.FLAT

        return cls(direction=direction, change_percent=change)


@dataclass(frozen=True, slots=True)
class DashboardCard:
    key: str
    title: str
    value: float | int | str
    unit: str | None = None
    subtitle: str | None = None
    progress: float | None = None
    trend: DashboardTrend | None = None
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.progress is not None and not 0 <= self.progress <= 100:
            raise ValueError("progress must be between 0 and 100")


@dataclass(frozen=True, slots=True)
class DashboardState:
    score: float
    cards: tuple[DashboardCard, ...]
    insights: tuple[str, ...]
    generated_at_iso: str

    def get_card(self, key: str) -> DashboardCard:
        for card in self.cards:
            if card.key == key:
                return card
        raise KeyError(key)
