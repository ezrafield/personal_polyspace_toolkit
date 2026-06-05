# Architecture

This template uses a layered structure:

- `src/api/`: input and output boundary.
- `src/services/`: business workflows and application logic.
- `src/models/`: domain data structures.
- `src/core/`: configuration and runtime setup.
- `src/utils/`: small reusable helpers.

## Boundaries
- API modules may call services.
- Services may use models and utilities.
- Models should not depend on API modules.
- Utilities should not know about product workflows.

## Data Flow
1. A caller reaches an API boundary.
2. The API validates input and delegates to a service.
3. The service performs business logic.
4. Models represent returned or persisted data.
5. The API formats the response.
