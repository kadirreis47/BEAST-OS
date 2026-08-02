
from __future__ import annotations

def km_to_steps(distance_km:float, step_length_m:float=0.78)->int:
    if distance_km <= 0 or step_length_m <= 0:
        raise ValueError("invalid input")
    return round((distance_km*1000)/step_length_m)
