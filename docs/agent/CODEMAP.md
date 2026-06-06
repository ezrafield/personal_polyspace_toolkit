# Code Map

Generated from the current `src/` directory.

## src/api/
Purpose: HTTP routes, request validation, response shaping, and transport boundaries.

Entry points:
- `src/api/__init__.py`
- `src/api/dependencies.py`
- `src/api/routes.py`

Tests:
- `tests/integration/test_api.py`

## src/core/
Purpose: Configuration, application setup, and cross-cutting primitives.

Entry points:
- `src/core/__init__.py`
- `src/core/config.py`

## src/models/
Purpose: Domain models and persistence-facing data structures.

Entry points:
- `src/models/__init__.py`
- `src/models/example.py`

Tests:
- `tests/unit/test_models.py`

## src/services/
Purpose: Business workflows and application logic.

Entry points:
- `src/services/__init__.py`
- `src/services/example_service.py`

Tests:
- `tests/unit/test_services.py`

## src/utils/
Purpose: Small shared helpers with no business ownership.

Entry points:
- `src/utils/__init__.py`
- `src/utils/strings.py`
