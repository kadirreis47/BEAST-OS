from datetime import date, datetime, timezone

import pytest

from beastos.storage import (
    Database,
    DailyMetric,
    DailyMetricRepository,
    HabitLog,
    HabitLogRepository,
)


@pytest.fixture
def database(tmp_path):
    db = Database(tmp_path / "beast.db")
    db.migrate()
    return db


def test_migrations_are_idempotent(database):
    database.migrate()
    with database.connect() as connection:
        versions = connection.execute("SELECT version FROM schema_migrations").fetchall()
    assert [row["version"] for row in versions] == ["0001_life_tracking"]


def test_daily_metric_upsert_and_range(database):
    repository = DailyMetricRepository(database)
    repository.upsert(DailyMetric(date(2026, 8, 1), "weight", 82.4, "kg"))
    repository.upsert(DailyMetric(date(2026, 8, 1), "weight", 81.9, "kg"))
    repository.upsert(DailyMetric(date(2026, 8, 2), "weight", 81.6, "kg"))

    stored = repository.get(date(2026, 8, 1), "weight")
    assert stored is not None
    assert stored.value == 81.9
    assert [item.value for item in repository.range("weight", date(2026, 8, 1), date(2026, 8, 2))] == [81.9, 81.6]


def test_habit_logs_are_returned_newest_first(database):
    repository = HabitLogRepository(database)
    repository.append(HabitLog("walk", datetime(2026, 8, 1, 8, tzinfo=timezone.utc), True, 5000))
    repository.append(HabitLog("walk", datetime(2026, 8, 2, 8, tzinfo=timezone.utc), False, 1200, "rain"))

    logs = repository.recent("walk")
    assert [log.value for log in logs] == [1200, 5000]
    assert logs[0].note == "rain"


def test_transaction_rolls_back(database):
    with pytest.raises(RuntimeError):
        with database.transaction() as connection:
            connection.execute(
                "INSERT INTO daily_metrics(metric_date, key, value, source) VALUES (?, ?, ?, ?)",
                ("2026-08-02", "sleep", 7.5, "manual"),
            )
            raise RuntimeError("force rollback")

    assert DailyMetricRepository(database).get(date(2026, 8, 2), "sleep") is None


def test_habit_log_requires_timezone():
    with pytest.raises(ValueError, match="timezone-aware"):
        HabitLog("walk", datetime(2026, 8, 2, 8), True)
