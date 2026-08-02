
from core.calculators.bmr import calculate_bmr

def test_bmr():
    assert calculate_bmr(80,180,30,"male")==1780.0
