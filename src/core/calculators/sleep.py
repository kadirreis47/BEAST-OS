
from __future__ import annotations

def sleep_debt(target_hours: float, actual_hours: float) -> float:
    if target_hours <= 0 or actual_hours < 0:
        raise ValueError("invalid values")
    return round(max(target_hours-actual_hours,0),2)

def sleep_efficiency(time_in_bed_minutes:int,time_asleep_minutes:int)->float:
    if time_in_bed_minutes<=0 or time_asleep_minutes<0:
        raise ValueError("invalid values")
    return round((time_asleep_minutes/time_in_bed_minutes)*100,2)
