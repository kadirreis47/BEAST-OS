
from src.core.calculators.sleep import sleep_debt,sleep_efficiency

def test_sleep():
    assert sleep_debt(8,6.5)==1.5
    assert sleep_efficiency(480,420)==87.5
