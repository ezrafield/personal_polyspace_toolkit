# Workflows

## Add A Feature
1. Read `docs/agent/INDEX.md`.
2. Read the relevant module card.
3. Inspect one similar implementation.
4. Add the smallest complete implementation.
5. Add or update focused tests.
6. Run targeted checks.
7. Update docs when behavior changes.

## Fix A Bug
1. Reproduce the bug with a failing test or command.
2. Read the module card for the affected area.
3. Patch the narrowest responsible code.
4. Add a regression test.
5. Run targeted tests.

## Refactor
1. Identify the behavior that must remain unchanged.
2. Read architecture and relevant module cards.
3. Prefer small mechanical steps.
4. Keep tests passing between steps when possible.
5. Avoid changing public contracts unless explicitly requested.
