import pytest
from thermostat_control import target_temperature, hvac_action, energy_alert

#Example test cases:
def test_away_mode():
    assert target_temperature("away", True, 12) == 16

def test_no_readings():
    assert energy_alert([], 10) == "ok"
def test_sleep_mode_before_6():
    assert target_temperature("sleep", True, 5) == 18


def test_sleep_mode_after_22():
    assert target_temperature("sleep", True, 22) == 18


def test_sleep_mode_daytime():
    assert target_temperature("sleep", True, 12) == 20


def test_unoccupied():
    assert target_temperature("home", False, 12) == 18


def test_morning_temperature():
    assert target_temperature("home", True, 7) == 22


def test_evening_temperature():
    assert target_temperature("home", True, 18) == 21


def test_normal_temperature():
    assert target_temperature("home", True, 12) == 20
def test_hvac_idle():
    assert hvac_action(20, 20.5, 25) == "idle"


def test_hvac_heat_boost():
    assert hvac_action(18, 22, 2) == "heat_boost"


def test_hvac_heat():
    assert hvac_action(18, 22, 15) == "heat"


def test_hvac_cool_boost():
    assert hvac_action(25, 20, 35) == "cool_boost"


def test_hvac_cool():
    assert hvac_action(25, 20, 25) == "cool"
def test_energy_alert_no_exceeding_readings():
    assert energy_alert([5, 8, 10], 10) == "ok"


def test_energy_alert_exactly_half_exceeding():
    assert energy_alert([15, 5], 10) == "warning"


def test_energy_alert_more_than_half_exceeding():
    assert energy_alert([15, 20, 5], 10) == "critical"


def test_energy_alert_one_exceeding():
    assert energy_alert([15, 5, 6], 10) == "warning"
#Write the rest of the test cases so that the code is 90- 100% covered.
