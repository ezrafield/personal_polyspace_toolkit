# docs-maintainer

## Purpose
Keep durable docs synchronized with project changes.

## Use When
- Public behavior changes.
- Module ownership changes.
- Commands change.
- API contracts change.
- Architecture decisions change.

## Workflow
1. Inspect changed files.
2. Check relevant docs:
   - `README.md`
   - `docs/agent/CODEMAP.md`
   - `docs/agent/module-cards/`
   - `docs/specs/`
   - `docs/adr/`
3. Update only durable documentation.
4. Leave task-local details in `.agent/tasks/`.

## Output
- Docs updated
- Docs checked but unchanged
- Remaining doc risks
