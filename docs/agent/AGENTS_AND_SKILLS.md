# Agents And Skills

This repository supports a small reusable agent kit:

- `.agents/skills/`: reusable Codex-style skills.
- `.claude/agents/`: Claude Code subagent templates.
- `scripts/`: deterministic tools that are cheaper and more auditable than agent reasoning.
- `docs/agent/`: routing docs and durable project context.

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
