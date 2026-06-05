# test-debugger

## Purpose
Debug failing tests or runtime errors.

## Use When
- A test fails.
- A runtime error appears.
- A bug can be reproduced with a focused command.

## Workflow
1. Run or inspect the smallest failing command.
2. Read the failure output.
3. Identify likely root cause.
4. Suggest or apply a minimal fix when allowed.
5. Re-run the same focused command.
6. Broaden test scope only after the focused check passes.

## Output
- Failing command
- Failure summary
- Root cause
- Fix summary
- Verification
