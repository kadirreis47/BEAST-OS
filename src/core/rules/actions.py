
from __future__ import annotations
from .base import RuleContext

def set_value(context: RuleContext, key: str, value)->None:
    context.values[key]=value

def increment(context: RuleContext, key: str, amount: int = 1)->None:
    context.values[key]=context.values.get(key,0)+amount
