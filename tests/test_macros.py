
from core.calculators.macros import calculate_macros

def test_macros():
    result=calculate_macros(2500,180)
    assert result["protein_g"]==180
    assert result["fat_g"]==69.4
    assert result["carb_g"]==288.9
