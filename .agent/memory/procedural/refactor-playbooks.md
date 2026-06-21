# Memory: Refactor Playbooks

Type: procedural
Scope: refactor
Confidence: medium
Last verified: 2026-06-19
Source task: .agent/tasks/README.md

## When to use

Use this memory before refactors, renames, or changes that cross module boundaries.

## Procedure

1. Read `docs/agent/ARCHITECTURE.md` and the relevant module cards.
2. Use Semble for natural-language discovery when available.
3. Use `rg` for exact symbols and paths.
4. Use Serena when references, declarations, diagnostics, or safe renames need language-server semantics.
5. Update docs or specs when public APIs or architectural behavior changes.
6. Run targeted tests first, then broader checks for shared behavior.

## Verification commands

```bash
make check-architecture-boundaries
make test-unit
```

## Related files

- `docs/agent/ARCHITECTURE.md`
- `docs/agent/CODE_SEARCH.md`
- `docs/agent/CONTEXT_ROUTER.md`

## Staleness triggers

- Module ownership changes.
- Architecture docs change.
- Serena or search tool guidance changes.
