---
name: c-compliance-loop
description: Drives an end-to-end Polyspace compliance loop for C translation units, from configuration through verified fixes.
license: MathWorks restricted BSD-3-Clause derivative
---
# C Compliance Loop

1. Read and validate `.polyspace-toolkit.json`. If it is missing, ask the user to choose at least
   one checker profile; never select a standard implicitly.
2. Select `.c` translation units only. For a header finding, identify a containing `.c` translation
   unit from `compile_commands.json` or the build system. Warn about ignored non-C entries.
3. Invoke `run-analysis` with the configured checker, build, options, and baseline paths.
4. For every finding, invoke `fix-findings`. Prefer a behavior-preserving code correction.
5. Compile and run the repository's targeted tests after each coherent fix batch.
6. Re-run Polyspace until the requested file or baseline scope is clean, or report the exact blocker.

Never change checker scope to make findings disappear. Never insert a justification without the
approval workflow in `justify-findings`.
