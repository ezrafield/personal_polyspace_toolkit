# Module: API

## Responsibility
Owns HTTP routes, request validation, response formatting, and boundary-level error handling.

## Key Files
- `src/api/routes.py`: route definitions
- `src/api/dependencies.py`: shared request dependencies
- `tests/integration/test_api.py`: integration coverage

## Public Interfaces
- Route handlers exposed by `src/api/routes.py`

## Rules
- Keep business logic out of route handlers.
- Delegate workflows to services.
- Update `docs/specs/api-contracts.md` when public contracts change.

## Common Tasks
- Add endpoint: inspect `routes.py`, service module card, and API contract specs.
- Change response shape: update specs and integration tests.

## Known Pitfalls
- Do not duplicate validation rules across route and service layers without a reason.
