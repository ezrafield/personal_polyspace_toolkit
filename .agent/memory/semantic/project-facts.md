# Memory: Project Facts

Type: semantic
Scope: project
Confidence: high
Last verified: 2026-06-19
Source task: .agent/tasks/README.md

## When to use

Use this memory when orienting on the template's purpose and baseline workflow.

## Content

- This repository is an agent-native project template for Codex, Claude Code, and similar coding agents.
- Agents should start with `AGENTS.md` or `CLAUDE.md`, route through `docs/agent/INDEX.md`, and load only relevant module cards or docs.
- `.agent/tasks/` is episodic memory: task-local notes and audit trails.
- `.agent/memory/` is long-term semantic and procedural memory that must be verified before use.

## Related files

- `AGENTS.md`
- `CLAUDE.md`
- `docs/agent/INDEX.md`
- `.agent/tasks/README.md`

## Staleness triggers

- Root agent entrypoints change.
- The context routing workflow changes.
- The task-log or memory folder layout changes.
