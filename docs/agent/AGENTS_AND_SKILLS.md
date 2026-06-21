# Agents And Skills

This repository supports a small reusable agent kit:

- `.agents/skills/`: reusable Codex-style skills.
- `.claude/agents/`: Claude Code subagent templates.
- `scripts/`: deterministic tools that are cheaper and more auditable than agent reasoning.
- `docs/agent/`: routing docs and durable project context.
- `.agent/memory/`: lightweight semantic and procedural memory.

## General Skills

| Skill | Use |
| --- | --- |
| `repo-navigator` | Find relevant files without broad scanning. |
| `safe-implementation` | Implement a feature or fix safely. |
| `test-debug-loop` | Reproduce, isolate, patch, and re-test failures. |
| `code-review` | Review code before merge. |
| `docs-sync` | Update durable docs after behavior changes. |
| `architecture-decision` | Compare options and record durable decisions. |
| `task-handoff` | Capture task state for continuation or audit. |
| `source-understanding` | Use Understand Anything for source discovery and onboarding. |
| `knowledge-graph-search` | Answer code questions through targeted graph search. |
| `agent-setup` | Bootstrap project-specific stack, command, codemap, module-card, and validation context. |

## Long-Term Memory

Use `.agent/memory/` after `docs/agent/INDEX.md` and before broad code search.
Memory should suggest likely files, workflows, and risks, but current source,
tests, and docs remain authoritative.

Promote task lessons manually:

1. Keep raw task state in `.agent/tasks/`.
2. Generate a candidate with `make extract-task-memory TASK=.agent/tasks/<task>.md`.
3. Review it for usefulness, safety, and staleness.
4. Move durable lessons into semantic or procedural memory.
5. Update `.agent/memory/index.json` and run `make audit-memory`.

## General Subagents

| Subagent | Use |
| --- | --- |
| `repo-researcher` | Read-only code discovery. |
| `code-reviewer` | Pre-merge review. |
| `test-debugger` | Failing tests and runtime errors. |
| `security-reviewer` | Auth, secrets, permissions, and sensitive data. |
| `docs-maintainer` | Documentation synchronization. |
| `understand-researcher` | Knowledge-graph backed source research. |

## When To Add Project-Specific Assets

Create project-specific skills or subagents only after repeated project-specific mistakes appear.

Good examples:
- Domain rules for regulated data.
- Evaluation runner for a specific AI pipeline.
- Migration reviewer for database-heavy projects.
- Release gatekeeper for deployment readiness.

Keep general skills reusable. Put domain knowledge in project-specific skills.
