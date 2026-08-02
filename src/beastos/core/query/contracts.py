from __future__ import annotations

from typing import Protocol, TypeVar

from .models import Query

ResultT = TypeVar("ResultT", covariant=True)
QueryT = TypeVar("QueryT", bound=Query[object], contravariant=True)


class QueryHandler(Protocol[QueryT, ResultT]):
    """Callable contract implemented by query handlers."""

    def __call__(self, query: QueryT) -> ResultT:
        ...


class QueryMiddleware(Protocol):
    """Middleware contract wrapping query execution."""

    def __call__(self, query: Query[object], call_next: "NextHandler") -> object:
        ...


class NextHandler(Protocol):
    def __call__(self, query: Query[object]) -> object:
        ...
