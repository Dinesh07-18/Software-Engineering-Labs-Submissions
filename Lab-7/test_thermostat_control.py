"""Hypothesis fuzz tests for thermostat input validation."""

import math

import pytest
from hypothesis import given, strategies as st

from thermostat_control import (
    average_temperature,
    parse_setpoint,
    schedule_slot,
)


def _looks_numeric(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(number)


TEXT_OR_NONE = st.one_of(st.text(), st.none())
FINITE_FLOATS = st.floats(
    min_value=-1000,
    max_value=1000,
    allow_nan=False,
    allow_infinity=False,
)


@given(TEXT_OR_NONE)
def test_parse_setpoint_fuzz_never_leaks_unexpected_exception(value):
    """Arbitrary inputs either parse to a finite number or fail cleanly."""
    try:
        result = parse_setpoint(value)
    except ValueError:
        return
    assert isinstance(result, float)
    assert math.isfinite(result)


@given(FINITE_FLOATS, st.sampled_from(["C", "c", "F", "f"]))
def test_parse_setpoint_valid_numeric_values(value, unit):
    """Valid generated temperatures are converted and remain finite."""
    result = parse_setpoint(f"{value:.8f}{unit}")
    assert math.isfinite(result)
    if unit.upper() == "C":
        assert result == round(float(f"{value:.8f}"), 1)


@given(st.text().filter(lambda value: not (
    value.strip() and value.strip()[-1:].upper() in {"C", "F"}
    and _looks_numeric(value.strip()[:-1])
)))
def test_parse_setpoint_rejects_malformed_text(value):
    with pytest.raises(ValueError):
        parse_setpoint(value)


@given(TEXT_OR_NONE)
def test_average_temperature_fuzz_never_leaks_unexpected_exception(value):
    """Arbitrary CSV input either returns a finite mean or fails cleanly."""
    try:
        result = average_temperature(value)
    except ValueError:
        return
    assert isinstance(result, float)
    assert math.isfinite(result)


@given(st.lists(FINITE_FLOATS, min_size=1, max_size=50))
def test_average_temperature_matches_generated_readings(values):
    csv_value = ",".join(repr(value) for value in values)
    result = average_temperature(csv_value)
    assert math.isclose(result, sum(values) / len(values), rel_tol=1e-12, abs_tol=1e-12)


@given(st.sampled_from(["", ",", "1,,2", ",1", "1,", "nan", "inf", "-inf"]))
def test_average_temperature_rejects_empty_or_non_finite_entries(value):
    with pytest.raises(ValueError):
        average_temperature(value)


@given(TEXT_OR_NONE)
def test_schedule_slot_fuzz_never_leaks_unexpected_exception(value):
    """Arbitrary time strings either produce a valid label or fail cleanly."""
    try:
        result = schedule_slot(value)
    except ValueError:
        return
    assert result.startswith(("night ", "day "))
    minute = int(result.split()[1])
    assert 0 <= minute <= 59


@given(st.integers(min_value=0, max_value=23), st.integers(min_value=0, max_value=59))
def test_schedule_slot_valid_time(hour, minute):
    result = schedule_slot(f"{hour:02d}:{minute:02d}")
    expected_period = "night" if hour < 6 else "day"
    assert result == f"{expected_period} {minute}"


@given(st.integers().filter(lambda value: value < 0 or value > 23),
       st.integers(min_value=0, max_value=59))
def test_schedule_slot_rejects_out_of_range_hour(hour, minute):
    with pytest.raises(ValueError):
        schedule_slot(f"{hour:02d}:{minute:02d}")


@given(st.integers(min_value=0, max_value=23),
       st.integers().filter(lambda value: value < 0 or value > 59))
def test_schedule_slot_rejects_out_of_range_minute(hour, minute):
    with pytest.raises(ValueError):
        schedule_slot(f"{hour:02d}:{minute:02d}")


@pytest.mark.parametrize("value", [None, "", "25", "25X", "abcC", "nanC", "infF"])
def test_parse_setpoint_known_invalid_values(value):
    with pytest.raises(ValueError):
        parse_setpoint(value)


@pytest.mark.parametrize("value", [None, "", " ", "1,,2", "abc", "nan", "inf"])
def test_average_temperature_known_invalid_values(value):
    with pytest.raises(ValueError):
        average_temperature(value)


@pytest.mark.parametrize("value", [None, "", "7", "24:00", "12:60", "-1:30", "7:3"])
def test_schedule_slot_known_invalid_values(value):
    with pytest.raises(ValueError):
        schedule_slot(value)
