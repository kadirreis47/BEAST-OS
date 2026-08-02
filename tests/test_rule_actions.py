
from src.core.rules.base import RuleContext
from src.core.rules.actions import set_value, increment

def test_actions():
    ctx=RuleContext({})
    set_value(ctx,"mode","focus")
    increment(ctx,"count")
    increment(ctx,"count",2)
    assert ctx.values=={"mode":"focus","count":3}
