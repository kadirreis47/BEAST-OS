
from beastos.analytics.scores import AnalyticsSnapshot
from beastos.analytics.insights import generate

def test_productivity():
    s=AnalyticsSnapshot(4,5,6,8,80,240)
    assert s.productivity>0
    assert isinstance(generate(s),list)
