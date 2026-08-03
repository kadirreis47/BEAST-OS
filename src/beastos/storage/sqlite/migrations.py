from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import sqlite3

from .database import SQLiteDatabase


@dataclass(frozen=True, slots=True)
class Migration:
    version: int
    name: str
    sql: str

    @property
    def checksum(self) -> str:
        return sha256(self.sql.encode("utf-8")).hexdigest()


class MigrationManager:
    def __init__(
        self,
        database: SQLiteDatabase,
        migrations: tuple[Migration, ...],
    ) -> None:
        self._database = database
        self._migrations = tuple(sorted(migrations, key=lambda item: item.version))

    def migrate(self) -> list[int]:
        applied_versions: list[int] = []

        with self._database.transaction() as connection:
            self._ensure_table(connection)
            existing = self._load_existing(connection)

            for migration in self._migrations:
                applied_checksum = existing.get(migration.version)
                if applied_checksum is not None:
                    if applied_checksum != migration.checksum:
                        raise RuntimeError(
                            f"migration checksum mismatch for version {migration.version}"
                        )
                    continue

                connection.executescript(migration.sql)
                connection.execute(
                    '''
                    INSERT INTO schema_migrations(version, name, checksum)
                    VALUES (?, ?, ?)
                    ''',
                    (
                        migration.version,
                        migration.name,
                        migration.checksum,
                    ),
                )
                applied_versions.append(migration.version)

        return applied_versions

    @staticmethod
    def _ensure_table(connection: sqlite3.Connection) -> None:
        connection.execute(
            '''
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                checksum TEXT NOT NULL,
                applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )

    @staticmethod
    def _load_existing(connection: sqlite3.Connection) -> dict[int, str]:
        rows = connection.execute(
            "SELECT version, checksum FROM schema_migrations"
        ).fetchall()
        return {
            int(row["version"]): str(row["checksum"])
            for row in rows
        }
