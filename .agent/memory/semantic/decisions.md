# Memory: Template Decisions

Type: semantic
Scope: project
Confidence: high
Last verified: 2026-06-19
Source task: .agent/tasks/README.md

## When to use

Use this memory when deciding whether to add dependencies or expand the agent kit.

## Content

- The memory layer is PlugMem-inspired but does not depend on PlugMem.
- The template favors lightweight Markdown, JSON indexes, and deterministic Python scripts over embeddings, graph databases, or model-hosting requirements.
- Memory promotion is manual: scripts can generate candidates, but promoted memory must be reviewed and intentionally indexed.
- Current source code, tests, and docs override memory when they conflict.

## Related files

- `docs/agent/MEMORY_POLICY.md`
- `docs/agent/MEMORY_PROMOTION_RULES.md`
- `.agent/memory/index.json`

## Staleness triggers

- A real memory engine, embedding index, or graph database is adopted.
- Promotion policy changes from manual to automatic or rule-assisted.
- Template dependency policy changes.
