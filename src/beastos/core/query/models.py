from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Generic, TypeVar
from uuid import UUID, uuid4

ResultT = TypeVar("ResultT")


@dataclass(frozen=True, slots=True, kw_only=True)
class Query(Generic[ResultT]):
    """Immutable base query carrying tracing metadata."""

    query_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
