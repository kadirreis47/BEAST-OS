from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .lifetime import Lifetime

Factory = Callable[["ServiceContainer"], Any]


@dataclass(slots=True)
class Registration:
    service_type: type[Any]
    factory: Factory
    lifetime: Lifetime
    instance: Any | None = None


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .container import ServiceContainer
