from __future__ import annotations

from .migrations import Migration


CORE_MIGRATIONS: tuple[Migration, ...] = (
    Migration(
        version=1,
        name="create_goals",
        sql='''
        CREATE TABLE IF NOT EXISTS goals (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            progress INTEGER NOT NULL CHECK(progress BETWEEN 0 AND 100),
            target_date TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            completed_at TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_goals_status
        ON goals(status);
        ''',
    ),
    Migration(
        version=2,
        name="create_habits",
        sql='''
        CREATE TABLE IF NOT EXISTS habits (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            frequency TEXT NOT NULL,
            status TEXT NOT NULL,
            target_per_period INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS habit_completions (
            habit_id TEXT NOT NULL,
            completed_on TEXT NOT NULL,
            PRIMARY KEY(habit_id, completed_on),
            FOREIGN KEY(habit_id) REFERENCES habits(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_habits_status
        ON habits(status);
        ''',
    ),
    Migration(
        version=3,
        name="create_planner",
        sql='''
        CREATE TABLE IF NOT EXISTS planner_days (
            day TEXT PRIMARY KEY
        );
        CREATE TABLE IF NOT EXISTS planner_blocks (
            id TEXT PRIMARY KEY,
            day TEXT NOT NULL,
            title TEXT NOT NULL,
            start_at TEXT NOT NULL,
            end_at TEXT NOT NULL,
            block_type TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            notes TEXT NOT NULL DEFAULT '',
            source_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY(day) REFERENCES planner_days(day) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_planner_blocks_day
        ON planner_blocks(day);
        ''',
    ),
)
