from __future__ import annotations

from collections.abc import Callable
from typing import TypeAlias

from .models import DomainEvent

EventHandler: TypeAlias = Callable[[DomainEvent], None]
EventMiddleware: TypeAlias = Callable[[DomainEvent, EventHandler], None]
