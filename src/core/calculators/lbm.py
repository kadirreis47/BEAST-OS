
from __future__ import annotations

def lean_body_mass(weight_kg: float, height_cm: float, sex: str) -> float:
    sex=sex.lower()
    if sex=="male":
        value=(0.407*weight_kg)+(0.267*height_cm)-19.2
    elif sex=="female":
        value=(0.252*weight_kg)+(0.473*height_cm)-48.3
    else:
        raise ValueError("sex must be 'male' or 'female'")
    return round(value,2)
