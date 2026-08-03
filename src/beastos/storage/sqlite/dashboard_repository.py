from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sqlite3
from threading import RLock


@dataclass(frozen=True, slots=True)
class DashboardSnapshotRecord:
    score: float
    goals_completed: int
    goals_total: int
    habits_completed: int
    habits_target: int
    planner_completion: float
    focus_minutes: int


class DashboardRepository:
    def __init__(self, database_path: str | Path) -> None:
        self._database_path = str(database_path)
        self._lock = RLock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                '''
                CREATE TABLE IF NOT EXISTS dashboard_snapshots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    score REAL NOT NULL,
                    goals_completed INTEGER NOT NULL,
                    goals_total INTEGER NOT NULL,
                    habits_completed INTEGER NOT NULL,
                    habits_target INTEGER NOT NULL,
                    planner_completion REAL NOT NULL,
                    focus_minutes INTEGER NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                '''
            )

    def save(self, snapshot: DashboardSnapshotRecord) -> int:
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                '''
                INSERT INTO dashboard_snapshots (
                    score,
                    goals_completed,
                    goals_total,
                    habits_completed,
                    habits_target,
                    planner_completion,
                    focus_minutes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''',
                (
                    snapshot.score,
                    snapshot.goals_completed,
                    snapshot.goals_total,
                    snapshot.habits_completed,
                    snapshot.habits_target,
                    snapshot.planner_completion,
                    snapshot.focus_minutes,
                ),
            )
            return int(cursor.lastrowid)

    def latest(self) -> DashboardSnapshotRecord | None:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                '''
                SELECT
                    score,
                    goals_completed,
                    goals_total,
                    habits_completed,
                    habits_target,
                    planner_completion,
                    focus_minutes
                FROM dashboard_snapshots
                ORDER BY id DESC
                LIMIT 1
                '''
            ).fetchone()

        if row is None:
            return None

        return DashboardSnapshotRecord(
            score=float(row["score"]),
            goals_completed=int(row["goals_completed"]),
            goals_total=int(row["goals_total"]),
            habits_completed=int(row["habits_completed"]),
            habits_target=int(row["habits_target"]),
            planner_completion=float(row["planner_completion"]),
            focus_minutes=int(row["focus_minutes"]),
        )
