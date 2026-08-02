import pytest

from core.calculators.body_fat import body_fat_us_navy


def test_us_navy_male_result() -> None:
    result = body_fat_us_navy(sex="male", height_cm=180, neck_cm=40, waist_cm=85)
    assert result == pytest.approx(14.53, abs=0.01)


def test_us_navy_female_requires_hip_measurement() -> None:
    with pytest.raises(ValueError, match="hip_cm required"):
        body_fat_us_navy(sex="female", height_cm=165, neck_cm=34, waist_cm=72)
