
from __future__ import annotations

def calculate_bmr(weight_kg: float, height_cm: float, age: int, sex: str) -> float:
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        raise ValueError("Invalid input.")
    sex = sex.lower()
    if sex == "male":
        value = 10*weight_kg + 6.25*height_cm - 5*age + 5
    elif sex == "female":
        value = 10*weight_kg + 6.25*height_cm - 5*age - 161
    else:
        raise ValueError("sex must be 'male' or 'female'")
    return round(value, 2)
