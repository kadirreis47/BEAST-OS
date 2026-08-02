
from src.core.rules.engine import RuleEngine
from src.core.rules.base import Rule, RuleContext

class DemoRule(Rule):
    priority=1
    def matches(self,c): return True
    def execute(self,c): c.values["ok"]=True

def test_engine():
    ctx=RuleContext({})
    eng=RuleEngine()
    eng.register(DemoRule())
    eng.evaluate(ctx)
    assert ctx.values["ok"] is True
