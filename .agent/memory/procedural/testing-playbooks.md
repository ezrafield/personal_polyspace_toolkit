# Memory: Testing Playbooks

Type: procedural
Scope: testing
Confidence: medium
Last verified: 2026-06-19
Source task: .agent/tasks/README.md

## When to use

Use this memory when choosing verification commands for behavior changes.

## Procedure

1. Start with the smallest test that covers the changed behavior.
2. Run unit tests before integration tests unless the change is integration-only.
3. Run lint and typecheck when code, public interfaces, or generated context changed.
4. Use compact Make targets when output may be noisy.
5. Record commands, failures, raw reruns, and skipped checks in the final response or task log.

## Verification commands

```bash
make test-unit
make lint
make typecheck
```

## Related files

- `Makefile`
- `scripts/run_targeted_tests.py`
- `docs/agent/COMMAND_OUTPUT_POLICY.md`

## Staleness triggers

- Make targets change.
- Test framework changes.
- Lint or typecheck commands change.
