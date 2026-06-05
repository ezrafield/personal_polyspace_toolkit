# Docs Sync

## Purpose
Update durable documentation only when behavior changes.

## Trigger
Use after implementation when public behavior, module ownership, commands, architecture, or API contracts changed.

## Check
- `README.md`
- `docs/agent/CODEMAP.md`
- `docs/agent/module-cards/`
- `docs/specs/api-contracts.md`
- `docs/adr/`
- `docs/agent/COMMANDS.md`

## Workflow
1. Identify what behavior or structure changed.
2. Update the smallest relevant docs.
3. Avoid copying task-local notes into durable docs.
4. Run `make validate-docs` when available.

## Output
- Docs inspected
- Docs changed
- Docs intentionally left unchanged
