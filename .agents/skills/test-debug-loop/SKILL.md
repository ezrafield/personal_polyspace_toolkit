# Test Debug Loop

## Purpose
Handle failing tests efficiently.

## Trigger
Use when tests fail, a runtime error appears, or the user asks to debug a failure.

## Workflow
1. Run the smallest failing test or reproduction.
2. Read the failure message.
3. Identify the probable root cause.
4. Patch minimally.
5. Re-run the same test.
6. Expand scope only after the focused check passes.

## Output
- Failing command
- Failure summary
- Root-cause hypothesis
- Patch summary
- Verification command

## Constraints
- Do not start with broad test suites unless no smaller check exists.
- Keep each loop focused on one failure.
