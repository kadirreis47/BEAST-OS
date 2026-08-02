
from core.calculators.heart_rate import max_heart_rate, training_zone
from core.calculators.steps import km_to_steps

def test_training_metrics():
    assert max_heart_rate(30)==190
    assert training_zone(30,0.7)==133
    assert km_to_steps(5)==6410
