# Module: Models

## Responsibility
Owns domain data structures and model-level behavior.

## Key Files
- `src/models/example.py`: sample domain model
- `tests/unit/test_models.py`: model coverage

## Public Interfaces
- Model classes and constructors exported from `src/models`

## Rules
- Keep transport-specific request and response objects out of models.
- Keep persistence decisions aligned with `docs/agent/module-cards/database.md`.
- Update tests when model invariants change.

## Common Tasks
- Add model: define the model, export it from the package when needed, and add unit tests.
- Change validation: update model tests and related API/service callers.

## Known Pitfalls
- Avoid placing workflow logic in models when it belongs in services.
