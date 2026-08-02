
from __future__ import annotations

from .bmr import calculate_bmr

_ACTIVITY={
    "sedentary":1.2,
    "light":1.375,
    "moderate":1.55,
    "active":1.725,
    "athlete":1.9,
}

def calculate_tdee(weight_kg:float,height_cm:float,age:int,sex:str,activity:str)->float:
    factor=_ACTIVITY.get(activity.lower())
    if factor is None:
        raise ValueError("invalid activity")
    return round(calculate_bmr(weight_kg,height_cm,age,sex)*factor,2)
