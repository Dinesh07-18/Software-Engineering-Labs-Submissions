# L6_L7_29 - Smart Thermostat Controller

**Lab 7: Fuzz Testing and Input Validation**

## About

A Python module for a smart thermostat controller. It processes temperature setpoints, calculates average sensor readings, and labels schedule slots.

This lab focuses on identifying input-validation defects through automated testing and improving application robustness.

## Lab 7 Objectives

- Identify input-validation bugs in the original implementation.
- Reproduce failures using automated tests.
- Improve input validation and error handling.
- Use fuzz and property-based testing to explore unexpected inputs.
- Verify the corrected implementation with an expanded test suite.

## Application Features

| Function | Description |
|---|---|
| `parse_setpoint()` | Parses temperature setpoints and handles Fahrenheit conversion. |
| `average_temperature()` | Calculates the average of comma-separated sensor readings. |
| `schedule_slot()` | Validates and classifies time values into schedule slots. |

## Files

| File / Folder | Description |
|---|---|
| `thermostat_control.py` | Corrected thermostat controller implementation. |
| `test_thermostat_control.py` | Expanded automated tests, including fuzz/property-based tests. |
| `SE_Lab07_report.pdf` | Lab 7 report containing methodology, findings, fixes, and test results. |
| `evidence/` | Screenshots and supplementary test output. |

## Testing

The original implementation was tested to reproduce input-validation failures.

| Implementation | Test Result |
|---|---|
| Original implementation | 21 failed, 10 passed |
| Corrected implementation | 31 passed |

The corrected implementation was verified using pytest and Hypothesis-based testing.

### Run the Tests

From the `lab7` directory:

```bash
python -m pytest -v
