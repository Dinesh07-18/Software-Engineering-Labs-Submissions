"""Input validation helpers for a smart thermostat controller."""

import math
import re


_SETPOINT_PATTERN = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)[cCfF]$")
_TIME_PATTERN = re.compile(r"^(\d{2}):(\d{2})$")


def parse_setpoint(text):
    """Parse a temperature such as '21.5C' or '70F' into Celsius.

    Raises ValueError for missing, malformed, non-finite, or unsupported values.
    """
    if not isinstance(text, str):
        raise ValueError("Setpoint must be a string ending in C or F.")

    normalized = text.strip()
    if not _SETPOINT_PATTERN.fullmatch(normalized):
        raise ValueError("Setpoint must be a number followed by C or F.")

    value = float(normalized[:-1])
    if not math.isfinite(value):
        raise ValueError("Setpoint must be a finite number.")

    if normalized[-1].upper() == "F":
        value = (value - 32) * 5 / 9
    return round(value, 1)


def average_temperature(readings_csv):
    """Return the mean of a non-empty CSV string of finite temperatures."""
    if not isinstance(readings_csv, str):
        raise ValueError("Readings must be supplied as a comma-separated string.")

    entries = readings_csv.split(",")
    if not entries or any(not entry.strip() for entry in entries):
        raise ValueError("At least one non-empty temperature reading is required.")

    try:
        values = [float(entry.strip()) for entry in entries]
    except ValueError as exc:
        raise ValueError("Every reading must be a valid number.") from exc

    if not all(math.isfinite(value) for value in values):
        raise ValueError("Temperature readings must be finite numbers.")

    # Divide before summing to avoid overflow for large finite readings.
    average = sum(value / len(values) for value in values)
    if not math.isfinite(average):
        raise ValueError("Average temperature is outside the supported numeric range.")
    return average


def schedule_slot(time_text):
    """Classify a valid 24-hour HH:MM time as night (before 06:00) or day."""
    if not isinstance(time_text, str):
        raise ValueError("Time must be a string in HH:MM format.")

    match = _TIME_PATTERN.fullmatch(time_text.strip())
    if match is None:
        raise ValueError("Time must use the HH:MM format.")

    hour, minute = (int(part) for part in match.groups())
    if not 0 <= hour <= 23 or not 0 <= minute <= 59:
        raise ValueError("Hour must be 00-23 and minute must be 00-59.")

    period = "night" if hour < 6 else "day"
    return f"{period} {minute}"


def main():
    """Run the interactive thermostat input demonstration."""
    print("==== Running parse_setpoint ====")
    setpoint_input = input("Enter a setpoint (e.g. 21.5C or 70F): ")
    try:
        print("Setpoint in Celsius:", parse_setpoint(setpoint_input))
    except ValueError as exc:
        print("Invalid setpoint:", exc)

    print("\n==== Running average_temperature ====")
    readings_input = input("Enter sensor readings as CSV (e.g. 20.5,21,22.5): ")
    try:
        print("Average Temperature:", average_temperature(readings_input))
    except ValueError as exc:
        print("Invalid readings:", exc)

    print("\n==== Running schedule_slot ====")
    time_input = input("Enter a time as HH:MM (e.g. 07:30): ")
    try:
        print("Schedule Slot:", schedule_slot(time_input))
    except ValueError as exc:
        print("Invalid time:", exc)


if __name__ == "__main__":
    main()
