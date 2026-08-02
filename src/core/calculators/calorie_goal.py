
from __future__ import annotations

from .tdee import calculate_tdee

_GOALS={
    "cut":-500,
    "maintain":0,
    "lean_bulk":250,
    "bulk":500,
}

def calorie_goal(weight_kg:float,height_cm:float,age:int,sex:str,activity:str,goal:str)->float:
    if goal not in _GOALS:
        raise ValueError("invalid goal")
    tdee=calculate_tdee(weight_kg,height_cm,age,sex,activity)
    return round(tdee+_GOALS[goal],2)
