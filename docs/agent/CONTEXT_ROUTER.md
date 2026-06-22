# Context Router

For non-trivial work:

1. Read `docs/agent/INDEX.md`.
2. Check `.agent/memory/index.json`; verify any useful memory against current source.
3. Read the relevant module card or `docs/agent/CODEMAP.md`.
4. Use Semble for behavior-level discovery when available.
5. Use `rg` for exact symbols, config keys, paths, client names, and policy text.
6. Use Serena only when reference or refactor semantics materially improve correctness.
7. Read full files after retrieval identifies likely targets.
8. Run targeted tests before the broad suite.

Use graph tooling for architecture impact and Repomix only for an explicitly requested external
repository export. Neither is part of the normal implementation loop.
