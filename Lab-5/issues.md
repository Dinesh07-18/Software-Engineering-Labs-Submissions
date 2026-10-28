\# Lab 5: Static Code Analysis — Digital Wallet



\## Issue Documentation



| No. | Tool | Issue / Type | Original Location | Description | Fix Applied |

|---:|---|---|---|---|---|

| 1 | Bandit | B324 — Weak hash | Line 14 | SHA-1 was used for PIN hashing. | Replaced SHA-1 with SHA-256 and used constant-time comparison with `hmac.compare\_digest`. |

| 2 | Bandit | B306 — Insecure temporary file | Line 60 | `tempfile.mktemp()` can create a race condition. | Replaced it with `tempfile.NamedTemporaryFile` and `delete=False`. |

| 3 | Bandit | B311 — Insecure random generator | Line 64 | `random.randint()` was used to generate an OTP. | Replaced it with `secrets.randbelow()`. |

| 4 | Bandit | B105 — Hard-coded secret | Lines 6–7 | Gateway secret and wallet PIN were embedded in the source code. | Added environment-variable configuration with demo-only fallback values. |

| 5 | Pylint | W0102 — Mutable default | Line 17 | The default list `log=\[]` could be shared between function calls. | Changed the default to `None` and initialized a new list inside the function. |

| 6 | Pylint | C0103 — Naming convention | Multiple lines | Function and variable names did not follow Python naming conventions. | Renamed functions and variables using `snake\_case`; moved the daily limit into a settings dictionary. |

| 7 | Pylint | C0114 / C0116 — Missing docstrings | Module and functions | The module and functions lacked documentation. | Added a module docstring and function docstrings. |

| 8 | Flake8 | E261, E225, E231, E305 | Lines 76–80 | The source contained spacing and blank-line violations. | Corrected whitespace, formatting and blank-line placement. |

| 9 | Pylint / Flake8 | Final newline and line endings | End of file | The file initially lacked a final newline and later had mixed line endings. | Normalized the file to consistent Windows CRLF line endings with a final newline. |



\## Before-and-After Results



| Tool | Before | After |

|---|---|---|

| Pylint | 5.69/10 | 10.00/10 |

| Bandit | 1 High, 1 Medium, 2 Low findings | No issues identified |

| Flake8 | 4 violations | No violations |



\## Conclusion



Static analysis helped identify security weaknesses, mutable default arguments, naming and documentation problems, and formatting violations. After making and checking the fixes, Pylint reached 10.00/10, Bandit reported no issues, and Flake8 reported no violations.



Note: The issue locations refer to the original source file and may differ from the updated file.



