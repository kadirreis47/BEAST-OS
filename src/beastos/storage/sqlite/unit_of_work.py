from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import sqlite3

from .database import SQLiteDatabase


class SQLiteUnitOfWork:
    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database

    @contextmanager
    def begin(self) -> Iterator[sqlite3.Connection]:
        with self._database.transaction() as connection:
            yield connection
