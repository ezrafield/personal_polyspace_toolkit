---
name: fix-findings
description: Explains and fixes Polyspace findings in C code, using justification only after explicit approval.
license: MathWorks restricted BSD-3-Clause derivative
---
# Fix C Findings

For each finding:

1. Preserve its exact family, acronym, message, location, and severity.
2. Invoke `find-checker-documentation` and understand the violated rule or defect condition.
3. Classify it as a genuine issue, likely false positive, intentional deviation, or blocked by
   missing build context. State the evidence.
4. For a genuine issue, apply the smallest behavior-preserving C fix. Compile, run targeted tests,
   and re-run `run-analysis` after a coherent batch.
5. For a false positive or intentional deviation, invoke `justify-findings`. Never suppress,
   weaken checker configuration, or insert an annotation automatically.

Stop and report when a fix changes a public interface, depends on target behavior not present in
the repository, or cannot be validated with the available build configuration.
