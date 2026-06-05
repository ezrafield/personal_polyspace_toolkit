# Module: Database

## Responsibility
Documents persistence-related decisions and model boundaries.

## Key Files
- `src/models/`
- `docs/adr/0002-database-choice.md`

## Public Interfaces
- Domain models exported by `src/models/`

## Rules
- Keep schema changes explicit and documented.
- Do not rewrite existing migrations without approval.
- Update ADRs when persistence strategy changes.

## Common Tasks
- Add model: inspect existing models and related tests.
- Change persistence behavior: inspect ADRs and integration coverage.

## Known Pitfalls
- Do not mix persistence concerns into API route handlers.
