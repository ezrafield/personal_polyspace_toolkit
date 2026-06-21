# Agent Memory

This folder stores lightweight long-term memory for future agents.

Memory is guidance, not source of truth. Always verify it against current code,
tests, and docs before editing.

## Types

- Semantic memory: stable project facts, conventions, and decisions.
- Procedural memory: reusable workflows and playbooks.
- Episodic memory: raw task logs under `.agent/tasks/`.

## Workflow

1. Capture task details in `.agent/tasks/`.
2. Run `make extract-task-memory TASK=.agent/tasks/<task>.md`.
3. Review the generated candidate under `.agent/memory/candidates/`.
4. Promote only durable, non-sensitive lessons into `semantic/` or `procedural/`.
5. Update `.agent/memory/index.json`.
6. Run `make audit-memory`.

Never promote secrets, credentials, customer data, raw stack traces with private
information, or one-off details that are unlikely to help future work.
