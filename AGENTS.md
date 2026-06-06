# AGENTS.md

## Project Purpose
This repository is a sample agent-native project template that demonstrates progressive context loading for Codex, Claude Code, and similar coding agents.

## Default Workflow
1. Understand the task.
2. Read `docs/agent/INDEX.md`.
3. Read only the relevant module card under `docs/agent/module-cards/`.
4. Make the smallest safe change.
5. Add or update tests when behavior changes.
6. Run targeted tests before broad tests.
7. Summarize changed files, commands run, and remaining risks.

## Context Rules
- Do not scan the whole repository unless the task requires it.
- Prefer `rg`, targeted file reads, and module cards.
- Do not load large docs unless referenced by `docs/agent/INDEX.md`.
- Keep changes scoped to the user request.

## Commands
- Install: `make install`
- Run app: `make dev`
- Unit tests: `make test-unit`
- Integration tests: `make test-integration`
- Lint: `make lint`
- Typecheck: `make typecheck`
- Docs map: `make docs-map`
- Agent setup: `make agent-setup`
- Agent audits: `make validate-agent-docs`, `make check-context-staleness`, `make audit-module-cards`

## Code Rules
- Follow existing patterns before introducing new abstractions.
- Do not add new dependencies without explicit justification.
- Do not change public APIs without updating docs or specs.
- Do not modify generated files manually.

## Definition Of Done
- Relevant tests pass.
- Lint and typecheck pass when applicable.
- Docs are updated if behavior changes.
- Final response includes files changed, commands run, and risks.
