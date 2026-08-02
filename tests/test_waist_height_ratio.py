
from core.calculators.waist_height_ratio import waist_height_ratio, classify_ratio

def test_ratio():
    r=waist_height_ratio(82,180)
    assert r==0.456
    assert classify_ratio(r)=="healthy"
