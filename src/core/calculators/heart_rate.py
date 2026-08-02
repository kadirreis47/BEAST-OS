
from __future__ import annotations

def max_heart_rate(age:int)->int:
    if age <= 0:
        raise ValueError("age must be positive")
    return 220 - age

def training_zone(age:int, intensity:float)->int:
    if not 0 < intensity <= 1:
        raise ValueError("intensity must be in (0,1]")
    return round(max_heart_rate(age) * intensity)
