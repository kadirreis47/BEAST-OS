from __future__ import annotations

from datetime import UTC, datetime, timedelta
from threading import Lock

from .models import ScheduledTask, TaskStatus
from .registry import TaskRegistry
from .store import SQLiteTaskStore


class SchedulerEngine:
    def __init__(self, registry: TaskRegistry, store: SQLiteTaskStore) -> None:
        self._registry = registry
        self._store = store
        self._run_lock = Lock()

    def schedule(self, task: ScheduledTask) -> None:
        self._registry.resolve(task.handler_name)
        self._store.save(task)

    def run_due(self, now: datetime | None = None, *, limit: int = 100) -> int:
        instant = now or datetime.now(UTC)
        if instant.tzinfo is None:
            raise ValueError("now must be timezone-aware")
        if not self._run_lock.acquire(blocking=False):
            return 0
        try:
            tasks = self._store.due(instant, limit=limit)
            for task in tasks:
                self._execute(task, instant)
            return len(tasks)
        finally:
            self._run_lock.release()

    def _execute(self, task: ScheduledTask, now: datetime) -> None:
        handler = self._registry.resolve(task.handler_name)
        task.status = TaskStatus.RUNNING
        task.last_run_at = now
        task.attempts += 1
        self._store.save(task)

        try:
            handler(dict(task.payload))
        except Exception as exc:
            task.last_error = f"{type(exc).__name__}: {exc}"
            if task.attempts >= task.retry_policy.max_attempts:
                task.status = TaskStatus.FAILED
                task.enabled = False
            else:
                task.status = TaskStatus.PENDING
                delay = task.retry_policy.delay_for(task.attempts)
                task.next_run_at = now + timedelta(seconds=delay)
        else:
            task.status = TaskStatus.SUCCEEDED
            task.attempts = 0
            task.last_error = None
            task.next_run_at = task.schedule.next_run(now)
        self._store.save(task)
