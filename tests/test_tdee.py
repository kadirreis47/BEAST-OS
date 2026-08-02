
from core.calculators.tdee import calculate_tdee

def test_tdee():
    assert calculate_tdee(80,180,30,"male","moderate")==2759.0
