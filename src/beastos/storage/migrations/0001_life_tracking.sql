CREATE TABLE IF NOT EXISTS daily_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_date TEXT NOT NULL,
    key TEXT NOT NULL CHECK(length(trim(key)) > 0),
    value REAL NOT NULL,
    unit TEXT,
    source TEXT NOT NULL DEFAULT 'manual',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(metric_date, key, source)
);

CREATE INDEX IF NOT EXISTS idx_daily_metrics_key_date
ON daily_metrics(key, metric_date);

CREATE TABLE IF NOT EXISTS habit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    habit_id TEXT NOT NULL CHECK(length(trim(habit_id)) > 0),
    logged_at TEXT NOT NULL,
    completed INTEGER NOT NULL CHECK(completed IN (0, 1)),
    value REAL,
    note TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_habit_logs_habit_time
ON habit_logs(habit_id, logged_at DESC);
