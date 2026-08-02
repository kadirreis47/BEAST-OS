
from __future__ import annotations

def body_fat_us_navy(*, sex:str, height_cm:float, neck_cm:float, waist_cm:float, hip_cm:float|None=None)->float:
    import math
    sex=sex.lower()
    if min(height_cm,neck_cm,waist_cm)<=0:
        raise ValueError("Measurements must be positive")
    if sex=="male":
        bf=495/(1.0324-0.19077*math.log10(waist_cm-neck_cm)+0.15456*math.log10(height_cm))-450
    elif sex=="female":
        if hip_cm is None or hip_cm<=0:
            raise ValueError("hip_cm required")
        bf=495/(1.29579-0.35004*math.log10(waist_cm+hip_cm-neck_cm)+0.22100*math.log10(height_cm))-450
    else:
        raise ValueError("invalid sex")
    return round(bf,2)
