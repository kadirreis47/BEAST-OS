
from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class RuleContext:
    values: dict[str, Any]

class Rule:
    priority:int=100
    def matches(self, context: RuleContext) -> bool:
        raise NotImplementedError
    def execute(self, context: RuleContext) -> None:
        raise NotImplementedError
