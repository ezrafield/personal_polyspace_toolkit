# Memory: Project Conventions

Type: semantic
Scope: project
Confidence: high
Last verified: 2026-06-19
Source task: .agent/tasks/README.md

## When to use

Use this memory before implementing non-trivial template or code changes.

## Content

- Prefer targeted reads, `rg`, Semble when available, module cards, and deterministic scripts over broad repository scans.
- Make the smallest safe change and update tests or docs when behavior changes.
- Run targeted tests before broad checks.
- Use compressed command output for noisy commands when RTK is available, and rerun raw output only when compressed output is unclear.
- Keep long-term memory concise, reusable, and free of secrets or private data.

## Related files

- `AGENTS.md`
- `docs/agent/CODE_SEARCH.md`
- `docs/agent/COMMAND_OUTPUT_POLICY.md`
- `docs/agent/MEMORY_POLICY.md`

## Staleness triggers

- Context retrieval policy changes.
- Command output policy changes.
- New required tools replace the existing default workflow.
