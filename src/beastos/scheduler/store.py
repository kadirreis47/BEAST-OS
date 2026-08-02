from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from threading import RLock

from .models import IntervalSchedule, RetryPolicy, ScheduledTask, TaskStatus


class SQLiteTaskStore:
    def __init__(self, database_path: str | Path) -> None:
        self._path = str(database_path)
        self._lock = RLock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS scheduled_tasks (
                    task_id TEXT PRIMARY KEY,
                    handler_name TEXT NOT NULL,
                    interval_seconds INTEGER NOT NULL CHECK(interval_seconds > 0),
                    payload_json TEXT NOT NULL,
                    retry_max_attempts INTEGER NOT NULL,
                    retry_base_delay_seconds INTEGER NOT NULL,
                    retry_multiplier REAL NOT NULL,
                    retry_max_delay_seconds INTEGER NOT NULL,
                    enabled INTEGER NOT NULL CHECK(enabled IN (0, 1)),
                    status TEXT NOT NULL,
                    attempts INTEGER NOT NULL,
                    next_run_at TEXT NOT NULL,
                    last_run_at TEXT,
                    last_error TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_due
                    ON scheduled_tasks(enabled, next_run_at);
                """
            )

    def save(self, task: ScheduledTask) -> None:
        values = (
            task.task_id,
            task.handler_name,
            task.schedule.seconds,
            json.dumps(task.payload, separators=(",", ":"), sort_keys=True),
            task.retry_policy.max_attempts,
            task.retry_policy.base_delay_seconds,
            task.retry_policy.multiplier,
            task.retry_policy.max_delay_seconds,
            int(task.enabled),
            task.status.value,
            task.attempts,
            task.next_run_at.isoformat(),
            task.last_run_at.isoformat() if task.last_run_at else None,
            task.last_error,
        )
        with self._lock, self._connect() as connection:
            connection.execute(
                """
                INSERT INTO scheduled_tasks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET
                    handler_name=excluded.handler_name,
                    interval_seconds=excluded.interval_seconds,
                    payload_json=excluded.payload_json,
                    retry_max_attempts=excluded.retry_max_attempts,
                    retry_base_delay_seconds=excluded.retry_base_delay_seconds,
                    retry_multiplier=excluded.retry_multiplier,
                    retry_max_delay_seconds=excluded.retry_max_delay_seconds,
                    enabled=excluded.enabled,
                    status=excluded.status,
                    attempts=excluded.attempts,
                    next_run_at=excluded.next_run_at,
                    last_run_at=excluded.last_run_at,
                    last_error=excluded.last_error
                """,
                values,
            )

    def get(self, task_id: str) -> ScheduledTask | None:
        with self._lock, self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM scheduled_tasks WHERE task_id = ?", (task_id,)
            ).fetchone()
        return self._from_row(row) if row else None

    def due(self, now: datetime, *, limit: int = 100) -> list[ScheduledTask]:
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if limit < 1:
            raise ValueError("limit must be at least 1")
        with self._lock, self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM scheduled_tasks
                WHERE enabled = 1 AND next_run_at <= ?
                ORDER BY next_run_at ASC, task_id ASC
                LIMIT ?
                """,
                (now.isoformat(), limit),
            ).fetchall()
        return [self._from_row(row) for row in rows]

    def delete(self, task_id: str) -> bool:
        with self._lock, self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM scheduled_tasks WHERE task_id = ?", (task_id,)
            )
            return cursor.rowcount > 0

    @staticmethod
    def _from_row(row: sqlite3.Row) -> ScheduledTask:
        return ScheduledTask(
            task_id=row["task_id"],
            handler_name=row["handler_name"],
            schedule=IntervalSchedule(row["interval_seconds"]),
            payload=json.loads(row["payload_json"]),
            retry_policy=RetryPolicy(
                max_attempts=row["retry_max_attempts"],
                base_delay_seconds=row["retry_base_delay_seconds"],
                multiplier=row["retry_multiplier"],
                max_delay_seconds=row["retry_max_delay_seconds"],
            ),
            enabled=bool(row["enabled"]),
            status=TaskStatus(row["status"]),
            attempts=row["attempts"],
            next_run_at=datetime.fromisoformat(row["next_run_at"]),
            last_run_at=(
                datetime.fromisoformat(row["last_run_at"])
                if row["last_run_at"]
                else None
            ),
            last_error=row["last_error"],
        )
