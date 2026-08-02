
from __future__ import annotations

_ACTIVITY_BONUS={
    "sedentary":0.0,
    "light":0.35,
    "moderate":0.7,
    "active":1.0,
    "athlete":1.5,
}

def daily_water_liters(weight_kg: float, activity: str="moderate")->float:
    if weight_kg<=0:
        raise ValueError("weight_kg must be positive")
    if activity not in _ACTIVITY_BONUS:
        raise ValueError("invalid activity")
    liters=(weight_kg*0.035)+_ACTIVITY_BONUS[activity]
    return round(liters,2)
