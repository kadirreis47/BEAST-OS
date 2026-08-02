from __future__ import annotations


class QueryError(RuntimeError):
    """Base exception for query bus failures."""


class QueryHandlerAlreadyRegisteredError(QueryError):
    """Raised when a handler is registered twice for the same query type."""


class QueryHandlerNotFoundError(QueryError):
    """Raised when no handler exists for a query type."""


class InvalidQueryHandlerError(QueryError):
    """Raised when a handler cannot be invoked safely."""
