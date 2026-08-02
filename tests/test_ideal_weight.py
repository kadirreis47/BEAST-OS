
from core.calculators.ideal_weight import devine

def test_devine():
    assert devine(180, "male") == 74.99
