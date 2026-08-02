
from __future__ import annotations

def calculate_macros(calories: float, protein_g: float, fat_percent: float=0.25) -> dict[str,float]:
    if calories <= 0 or protein_g < 0:
        raise ValueError("invalid input")
    fat_g = round((calories * fat_percent) / 9, 1)
    protein_cal = protein_g * 4
    fat_cal = fat_g * 9
    carb_g = round((calories - protein_cal - fat_cal) / 4, 1)
    if carb_g < 0:
        raise ValueError("protein exceeds calorie target")
    return {
        "protein_g": round(protein_g,1),
        "fat_g": fat_g,
        "carb_g": carb_g,
    }
