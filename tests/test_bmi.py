
from core.calculators.bmi import calculate_bmi, classify_bmi

def test_bmi():
    assert calculate_bmi(80,180)==24.69
    assert classify_bmi(24.69)=="normal"
