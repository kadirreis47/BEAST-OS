
from __future__ import annotations

def waist_height_ratio(waist_cm: float, height_cm: float) -> float:
    if waist_cm <= 0 or height_cm <= 0:
        raise ValueError("Measurements must be positive")
    return round(waist_cm / height_cm, 3)

def classify_ratio(ratio: float) -> str:
    if ratio < 0.40:
        return "under"
    if ratio < 0.50:
        return "healthy"
    if ratio < 0.60:
        return "overweight_risk"
    return "high_risk"
