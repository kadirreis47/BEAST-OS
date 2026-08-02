
from __future__ import annotations
from .base import Rule, RuleContext

class RuleEngine:
    def __init__(self)->None:
        self._rules:list[Rule]=[]

    def register(self, rule:Rule)->None:
        self._rules.append(rule)
        self._rules.sort(key=lambda r:r.priority)

    def evaluate(self, context:RuleContext)->None:
        for rule in self._rules:
            if rule.matches(context):
                rule.execute(context)
