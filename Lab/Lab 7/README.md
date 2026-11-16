# Lab 7 – Fuzzing for Input Validation Bugs

## Objective
To identify and fix input validation bugs using fuzz testing with the Hypothesis library.

## Description
This lab focuses on applying property-based testing to the Bus Transit Fare Management System. Hypothesis was used to generate unexpected and invalid inputs to identify bugs in the application.

## Work Completed
1. Executed the original `processor.py` application.
2. Installed and used Hypothesis and Pytest.
3. Created `test_processor.py` to perform fuzz testing.
4. Identified input validation issues in the application.
5. Fixed the bugs in `processor.py`.
6. Executed the fuzz tests again to verify the corrections.

## Functions Tested
- `parse_transit_corridor`
- `lookup_concession_discount`
- `compute_passenger_density`

## Testing Results
Initially, fuzz testing identified failures in all three functions. After fixing the input validation issues, all three test cases passed successfully.

## Files Included
- `processor.py` – Fixed application.
- `test_processor.py` – Hypothesis fuzz testing code.
- `Lab7_FuzzTesting_Report.pdf` – Screenshots showing the testing process and results.

## Tools Used
- Python
- Hypothesis
- Pytest
