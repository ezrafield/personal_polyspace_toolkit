# Memory: Conventions

Type: semantic
Scope: project
Confidence: high
Last verified: 2026-06-22
Source task: .agent/tasks/README.md

## When to use
Use before changing setup, configuration, or Polyspace workflow behavior.

## Content
- Treat unknown client entries and skill directories as user-owned.
- Keep telemetry opt-in and state secret-free.
- Require explicit profiles, C translation units, and human approval for justifications and generated
  executable runs.
- Use targeted tests before the three-OS integration suite.
- Current source, schemas, tests, and installed-release documentation override memory.

## Related files
- `AGENTS.md`
- `docs/agent/PITFALLS.md`
- `tests/`

## Staleness triggers
Safety policy, supported clients, or test strategy changes.
