
from __future__ import annotations

def devine(height_cm: float, sex: str) -> float:
    if height_cm <= 0:
        raise ValueError("height_cm must be positive")
    inches = height_cm / 2.54
    over = max(0.0, inches - 60)
    sex = sex.lower()
    if sex == "male":
        return round(50 + 2.3 * over, 2)
    if sex == "female":
        return round(45.5 + 2.3 * over, 2)
    raise ValueError("sex must be 'male' or 'female'")
