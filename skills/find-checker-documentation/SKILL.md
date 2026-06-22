---
name: find-checker-documentation
description: Finds official documentation for Polyspace C defects and coding rules.
license: MathWorks restricted BSD-3-Clause derivative
---
# Find C Checker Documentation

Preserve the exact finding family and acronym. Prefer `get_polyspace_documentation` when it can
return the installed-release documentation. Otherwise use official MathWorks documentation.

Supported families include Polyspace defects, MISRA C:2012, MISRA C:2023, CERT C, and CWE. Do not
construct a page URL from memory when the family or acronym is ambiguous. Return the documentation
URL, checker summary, risky condition, and the detail relevant to the reported line.
