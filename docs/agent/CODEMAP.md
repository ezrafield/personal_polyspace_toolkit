# Code Map

This file is intended to be generated or maintained by `scripts/generate_codemap.py`.

## src/api/
Purpose: HTTP routes, request validation, and response shaping.

Entry points:
- `src/api/routes.py`
- `src/api/dependencies.py`

Tests:
- `tests/integration/test_api.py`

Common changes:
- Add endpoint
- Update response schema
- Add auth dependency

## src/services/
Purpose: business logic layer.

Entry points:
- `src/services/example_service.py`

Rules:
- No direct HTTP logic here.
- No direct environment variable access here.

## src/models/
Purpose: domain models and persistence-facing data structures.

Entry points:
- `src/models/example.py`

Tests:
- `tests/unit/test_models.py`

## src/core/
Purpose: configuration, application setup, and cross-cutting primitives.

Entry points:
- `src/core/config.py`

## src/utils/
Purpose: small shared helpers with no business ownership.

Entry points:
- `src/utils/strings.py`
