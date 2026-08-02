from datetime import UTC, datetime, timedelta

from beastos.scheduler import IntervalSchedule, ScheduledTask, SQLiteTaskStore


def test_store_round_trip_and_due_query(tmp_path) -> None:
    store = SQLiteTaskStore(tmp_path / "scheduler.db")
    now = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)
    task = ScheduledTask(
        task_id="daily-review",
        handler_name="review",
        schedule=IntervalSchedule(3600),
        payload={"scope": "day"},
        next_run_at=now - timedelta(seconds=1),
    )
    store.save(task)

    loaded = store.get("daily-review")
    assert loaded is not None
    assert loaded.payload == {"scope": "day"}
    assert [item.task_id for item in store.due(now)] == ["daily-review"]
    assert store.delete("daily-review") is True
    assert store.get("daily-review") is None
