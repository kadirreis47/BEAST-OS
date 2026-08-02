
from core.calculators.pace import minutes_per_km, kmh

def test_running_metrics():
    assert minutes_per_km(5, 25) == 5.0
    assert kmh(5, 25) == 12.0
