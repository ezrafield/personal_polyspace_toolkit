# Module: Core

## Responsibility
Owns project configuration and other cross-cutting runtime primitives.

## Key Files
- `src/core/config.py`: configuration defaults and access helpers

## Public Interfaces
- Configuration objects and helpers exported from `src/core`

## Rules
- Keep environment parsing centralized.
- Do not import API route handlers, services, or tests from core runtime modules.
- Document behavior changes that affect deployment or local setup.

## Common Tasks
- Add configuration: update `src/core/config.py`, command docs, and relevant tests.
- Change defaults: check callers and update setup notes.

## Known Pitfalls
- Avoid reading environment variables directly from feature modules when a core helper should own that concern.
