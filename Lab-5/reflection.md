\# Lab 5: Static Code Analysis — Reflection



\## 1. What is static code analysis, and how does it help improve code quality?



Static code analysis examines source code without executing the program. It helps identify potential bugs, security weaknesses, naming problems, missing documentation and formatting violations. In this lab, Pylint, Bandit and Flake8 helped improve the quality, security and readability of the Digital Wallet program.



\## 2. What types of issues did Pylint, Bandit and Flake8 identify?



Pylint identified missing docstrings, inconsistent naming conventions and a mutable default argument. Bandit identified the use of SHA-1 for PIN hashing, insecure temporary-file creation, a non-cryptographic random generator for OTP generation and hard-coded credentials. Flake8 identified whitespace and blank-line violations.



\## 3. Which issue was the most important to fix, and why?



The weak SHA-1 hashing issue was important because the program used it to process PINs. I replaced SHA-1 with SHA-256 and used `hmac.compare\_digest` for comparison. This improves the hash choice and comparison behavior, although SHA-256 alone is not sufficient for production PIN storage; a salted, deliberately slow password-hashing method is preferable.



\## 4. How did static analysis improve the program, and what did you learn?



Static analysis helped me identify and fix security, maintainability and formatting issues. The original Pylint score was 5.69/10, while the final score was 10.00/10. Bandit reported no issues after the changes, and Flake8 reported no violations. I learned that running multiple static-analysis tools helps identify different categories of problems and that the reports should be rerun after making changes to verify the fixes.



