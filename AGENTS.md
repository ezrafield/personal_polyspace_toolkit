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

## Context Retrieval Policy
For non-trivial code tasks, do not scan the whole repository.

Use this order:
1. Read `docs/agent/INDEX.md`.
2. Read the relevant module card or `docs/agent/CODEMAP.md`.
3. Use Semble for natural-language code search:
   - `semble search "<task>" . --content code`
   - `semble search "<task>" . --content all` when docs/config may matter
4. Use `rg` for exact symbol/string confirmation.
5. Use Serena when symbol references, declarations, implementations, diagnostics, or safe refactors are needed.
6. Read full files only after retrieval identifies likely relevant targets.
7. Before editing, summarize:
   - selected files
   - why they are relevant
   - uncertainty/risk
8. After editing, run targeted tests first.

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
- Compact output helpers: `make git-status`, `make git-diff`, `make test-unit-compact`, `make lint-compact`, `make typecheck-compact`

## Command Output Rules
For noisy terminal commands, prefer compressed output.

Use RTK when available:
- `rtk git status`
- `rtk git diff`
- `rtk grep`
- `rtk find`
- `rtk pytest`
- `rtk cargo test`
- `rtk npm test`
- `rtk tsc`
- `rtk eslint`

If compressed output is incomplete or suspicious:
1. Rerun the specific command in raw mode.
2. Inspect only the relevant failing section.
3. Mention the rerun in the final command summary.

Do not hide failures. Test failures, stack traces, exit codes, and actionable errors must remain visible.

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
