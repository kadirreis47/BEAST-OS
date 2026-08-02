import pytest

from core.calculators.lbm import lean_body_mass


def test_boer_male_result() -> None:
    assert lean_body_mass(80, 180, "male") == pytest.approx(61.42)


def test_boer_female_result() -> None:
    assert lean_body_mass(65, 165, "female") == pytest.approx(46.12)
