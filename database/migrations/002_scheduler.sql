CREATE TABLE IF NOT EXISTS scheduled_tasks (
    task_id TEXT PRIMARY KEY,
    handler_name TEXT NOT NULL,
    interval_seconds INTEGER NOT NULL CHECK(interval_seconds > 0),
    payload_json TEXT NOT NULL,
    retry_max_attempts INTEGER NOT NULL CHECK(retry_max_attempts > 0),
    retry_base_delay_seconds INTEGER NOT NULL CHECK(retry_base_delay_seconds >= 0),
    retry_multiplier REAL NOT NULL CHECK(retry_multiplier >= 1),
    retry_max_delay_seconds INTEGER NOT NULL CHECK(retry_max_delay_seconds >= 0),
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0, 1)),
    status TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0 CHECK(attempts >= 0),
    next_run_at TEXT NOT NULL,
    last_run_at TEXT,
    last_error TEXT
);

CREATE INDEX IF NOT EXISTS idx_scheduled_tasks_due
    ON scheduled_tasks(enabled, next_run_at);
