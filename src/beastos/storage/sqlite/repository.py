from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from .database import SQLiteDatabase

EntityT = TypeVar("EntityT")


class SQLiteRepository(ABC, Generic[EntityT]):
    def __init__(self, database: SQLiteDatabase) -> None:
        self._database = database

    @property
    def database(self) -> SQLiteDatabase:
        return self._database
