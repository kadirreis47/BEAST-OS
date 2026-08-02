
from core.calculators.water import daily_water_liters

def test_daily_water():
    assert daily_water_liters(80,"moderate")==3.5
