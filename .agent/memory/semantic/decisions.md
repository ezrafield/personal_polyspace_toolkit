# Memory: Decisions

Type: semantic
Scope: project
Confidence: high
Last verified: 2026-06-22
Source task: .agent/tasks/README.md

## When to use
Use when proposed work changes dependencies, client support, release selection, or model integration.

## Content
- `tomlkit` is the sole runtime dependency because format-preserving Codex TOML edits should not use
  ad hoc string manipulation.
- MCP server setup defaults to the release tested with the toolkit, not the latest network release.
- Client registration is user-scoped.
- Qwen Code uses manually merged settings and a later-provided local endpoint; no extension or writer.
- The public derivative retains the MathWorks-product-only license condition and clear attribution.

## Related files
- `pyproject.toml`
- `UPSTREAM.md`
- `docs/setup/qwen-local.md`

## Staleness triggers
Runtime dependencies, licensing, Qwen integration, or release policy changes.
