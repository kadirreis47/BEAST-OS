from pathlib import Path

import pytest

from beastos.storage.sqlite import (
    Migration,
    MigrationManager,
    SQLiteDatabase,
)
from beastos.storage.sqlite.schema import CORE_MIGRATIONS
from beastos.storage.sqlite.unit_of_work import SQLiteUnitOfWork


def test_database_transaction_commit(tmp_path: Path):
    database = SQLiteDatabase(tmp_path / "beast.db")
    database.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")

    with database.transaction() as connection:
        connection.execute(
            "INSERT INTO items(name) VALUES (?)",
            ("alpha",),
        )

    row = database.query_one("SELECT name FROM items WHERE id = 1")
    assert row["name"] == "alpha"


def test_database_transaction_rollback(tmp_path: Path):
    database = SQLiteDatabase(tmp_path / "beast.db")
    database.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")

    with pytest.raises(RuntimeError):
        with database.transaction() as connection:
            connection.execute(
                "INSERT INTO items(name) VALUES (?)",
                ("alpha",),
            )
            raise RuntimeError("fail")

    assert database.query_one("SELECT * FROM items") is None


def test_core_migrations_are_applied_once(tmp_path: Path):
    database = SQLiteDatabase(tmp_path / "beast.db")
    manager = MigrationManager(database, CORE_MIGRATIONS)

    first = manager.migrate()
    second = manager.migrate()

    assert first == [1, 2, 3]
    assert second == []
    assert database.query_one(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='goals'"
    ) is not None
    assert database.query_one(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='habits'"
    ) is not None
    assert database.query_one(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='planner_blocks'"
    ) is not None


def test_migration_checksum_change_is_rejected(tmp_path: Path):
    database = SQLiteDatabase(tmp_path / "beast.db")
    original = Migration(version=1, name="one", sql="CREATE TABLE one(id INTEGER);")
    changed = Migration(version=1, name="one", sql="CREATE TABLE two(id INTEGER);")

    MigrationManager(database, (original,)).migrate()

    with pytest.raises(RuntimeError, match="checksum mismatch"):
        MigrationManager(database, (changed,)).migrate()


def test_unit_of_work_uses_database_transaction(tmp_path: Path):
    database = SQLiteDatabase(tmp_path / "beast.db")
    database.execute("CREATE TABLE items(id INTEGER PRIMARY KEY, name TEXT)")
    unit_of_work = SQLiteUnitOfWork(database)

    with unit_of_work.begin() as connection:
        connection.execute(
            "INSERT INTO items(name) VALUES (?)",
            ("beta",),
        )

    row = database.query_one("SELECT name FROM items WHERE id = 1")
    assert row["name"] == "beta"
