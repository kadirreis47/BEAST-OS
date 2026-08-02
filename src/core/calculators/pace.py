
from __future__ import annotations

def minutes_per_km(distance_km: float, duration_minutes: float) -> float:
    if distance_km <= 0 or duration_minutes <= 0:
        raise ValueError("distance_km and duration_minutes must be positive")
    return round(duration_minutes / distance_km, 2)

def kmh(distance_km: float, duration_minutes: float) -> float:
    hours = duration_minutes / 60
    return round(distance_km / hours, 2)
