---
name: generate-c-pstunit-tests
description: Plans, writes, builds, and approval-gates execution of C tests using Polyspace PSTUnit.
license: MathWorks restricted BSD-3-Clause derivative
---
# Generate C PSTUnit Tests

1. Inspect the C function, its callers, data types, state, and build configuration.
2. Present a test plan covering nominal, error, boundary, null-pointer, integer-limit, and stateful
   behavior. Wait for approval before authoring tests.
3. Read `reference/xunit_api_c.md`, include `pstunit.h`, register every test with `PST_ADD_TEST`, and
   return `PST_MAIN(argc, argv)` from `main`.
4. Build with the same C compiler, defines, include paths, target assumptions, and warnings as the
   production code. Use `pstest.c` for R2026b+ or `pstunit.c` for earlier supported releases.
5. Show the exact executable and invocation. Wait for explicit approval before running generated code.
6. Fix build or test failures and repeat validation without weakening assertions.
