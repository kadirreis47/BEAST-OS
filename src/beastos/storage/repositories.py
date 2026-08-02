from __future__ import annotations

from datetime import date, datetime

from .database import Database
from .records import DailyMetric, HabitLog, utc_now_iso


class DailyMetricRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def upsert(self, metric: DailyMetric) -> None:
        with self.database.transaction() as connection:
            connection.execute(
                """
                INSERT INTO daily_metrics(metric_date, key, value, unit, source, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(metric_date, key, source) DO UPDATE SET
                    value = excluded.value,
                    unit = excluded.unit,
                    updated_at = excluded.updated_at
                """,
                (
                    metric.metric_date.isoformat(),
                    metric.key,
                    metric.value,
                    metric.unit,
                    metric.source,
                    utc_now_iso(),
                ),
            )

    def get(self, metric_date: date, key: str, source: str = "manual") -> DailyMetric | None:
        with self.database.connect() as connection:
            row = connection.execute(
                """
                SELECT metric_date, key, value, unit, source
                FROM daily_metrics
                WHERE metric_date = ? AND key = ? AND source = ?
                """,
                (metric_date.isoformat(), key, source),
            ).fetchone()
        if row is None:
            return None
        return DailyMetric(
            metric_date=date.fromisoformat(row["metric_date"]),
            key=row["key"],
            value=row["value"],
            unit=row["unit"],
            source=row["source"],
        )

    def range(self, key: str, start: date, end: date) -> list[DailyMetric]:
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT metric_date, key, value, unit, source
                FROM daily_metrics
                WHERE key = ? AND metric_date BETWEEN ? AND ?
                ORDER BY metric_date ASC, source ASC
                """,
                (key, start.isoformat(), end.isoformat()),
            ).fetchall()
        return [
            DailyMetric(
                metric_date=date.fromisoformat(row["metric_date"]),
                key=row["key"],
                value=row["value"],
                unit=row["unit"],
                source=row["source"],
            )
            for row in rows
        ]


class HabitLogRepository:
    def __init__(self, database: Database) -> None:
        self.database = database

    def append(self, log: HabitLog) -> int:
        with self.database.transaction() as connection:
            cursor = connection.execute(
                """
                INSERT INTO habit_logs(habit_id, logged_at, completed, value, note)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    log.habit_id,
                    log.logged_at.isoformat(),
                    int(log.completed),
                    log.value,
                    log.note,
                ),
            )
            return int(cursor.lastrowid)

    def recent(self, habit_id: str, limit: int = 30) -> list[HabitLog]:
        if limit <= 0:
            raise ValueError("limit must be positive")
        with self.database.connect() as connection:
            rows = connection.execute(
                """
                SELECT habit_id, logged_at, completed, value, note
                FROM habit_logs
                WHERE habit_id = ?
                ORDER BY logged_at DESC, id DESC
                LIMIT ?
                """,
                (habit_id, limit),
            ).fetchall()
        return [
            HabitLog(
                habit_id=row["habit_id"],
                logged_at=datetime.fromisoformat(row["logged_at"]),
                completed=bool(row["completed"]),
                value=row["value"],
                note=row["note"],
            )
            for row in rows
        ]
