
from core.calculators.calorie_goal import calorie_goal

def test_goal():
    assert calorie_goal(80,180,30,"male","moderate","cut")==2259.0
    assert calorie_goal(80,180,30,"male","moderate","bulk")==3259.0
