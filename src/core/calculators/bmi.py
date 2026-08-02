
from __future__ import annotations

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if weight_kg <= 0 or height_cm <= 0:
        raise ValueError("weight_kg and height_cm must be positive")
    height_m = height_cm / 100
    return round(weight_kg / (height_m * height_m), 2)

def classify_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "overweight"
    return "obese"
