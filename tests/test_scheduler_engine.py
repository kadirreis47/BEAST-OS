from datetime import UTC, datetime, timedelta

from beastos.scheduler import (
    IntervalSchedule,
    RetryPolicy,
    ScheduledTask,
    SchedulerEngine,
    SQLiteTaskStore,
    TaskRegistry,
    TaskStatus,
)


def test_engine_executes_and_reschedules_successful_task(tmp_path) -> None:
    calls: list[dict[str, str]] = []
    registry = TaskRegistry()
    registry.register("capture", calls.append)
    store = SQLiteTaskStore(tmp_path / "scheduler.db")
    engine = SchedulerEngine(registry, store)
    now = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)
    engine.schedule(
        ScheduledTask(
            task_id="capture-1",
            handler_name="capture",
            schedule=IntervalSchedule(60),
            payload={"kind": "focus"},
            next_run_at=now,
        )
    )

    assert engine.run_due(now) == 1
    task = store.get("capture-1")
    assert calls == [{"kind": "focus"}]
    assert task is not None
    assert task.status is TaskStatus.SUCCEEDED
    assert task.next_run_at == now + timedelta(seconds=60)


def test_engine_retries_then_disables_failed_task(tmp_path) -> None:
    registry = TaskRegistry()

    def fail(_: dict[str, object]) -> None:
        raise RuntimeError("boom")

    registry.register("fail", fail)
    store = SQLiteTaskStore(tmp_path / "scheduler.db")
    engine = SchedulerEngine(registry, store)
    now = datetime(2026, 8, 2, 12, 0, tzinfo=UTC)
    engine.schedule(
        ScheduledTask(
            task_id="failure",
            handler_name="fail",
            schedule=IntervalSchedule(60),
            retry_policy=RetryPolicy(max_attempts=2, base_delay_seconds=5),
            next_run_at=now,
        )
    )

    engine.run_due(now)
    pending = store.get("failure")
    assert pending is not None
    assert pending.status is TaskStatus.PENDING
    assert pending.next_run_at == now + timedelta(seconds=5)

    engine.run_due(now + timedelta(seconds=5))
    failed = store.get("failure")
    assert failed is not None
    assert failed.status is TaskStatus.FAILED
    assert failed.enabled is False
    assert failed.last_error == "RuntimeError: boom"
