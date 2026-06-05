# Module: Services

## Responsibility
Owns business workflows and application logic.

## Key Files
- `src/services/example_service.py`: sample service
- `tests/unit/test_services.py`: service tests

## Public Interfaces
- `ExampleService`

## Rules
- Services should not import framework-specific request objects.
- Services should receive dependencies explicitly.
- Keep persistence and transport concerns behind boundaries.

## Common Tasks
- Add workflow: add a service method and unit tests.
- Change business rule: update tests and related product requirements.

## Known Pitfalls
- Do not read environment variables directly inside service methods.
