# Module: Utils

## Responsibility
Provides small reusable helpers that are not tied to a product workflow.

## Key Files
- `src/utils/strings.py`: string helper examples

## Public Interfaces
- Utility functions exported from `src/utils`

## Rules
- Keep utilities narrow and dependency-light.
- Prefer module-specific helpers when logic is only used in one boundary.
- Add unit tests for helpers with branching or edge cases.

## Common Tasks
- Add helper: check for an existing local helper first, then add focused tests.
- Change helper behavior: search all callers before updating expectations.

## Known Pitfalls
- Avoid turning `utils` into a dumping ground for business logic.
