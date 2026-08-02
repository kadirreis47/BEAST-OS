from __future__ import annotations

from enum import StrEnum


class Lifetime(StrEnum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
