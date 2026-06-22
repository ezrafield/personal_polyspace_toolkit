# Module: Clients

## Responsibility
Owns user-scoped Codex and Claude MCP configuration plus automated skill destinations.

## Rules
- Codex TOML is parsed and written structurally.
- Claude is configured through its native CLI.
- Preserve unrelated entries and refuse un-restorable existing registrations.
- Qwen is read-only verification and documentation; no writer or extension.

## Tests
Config preservation, exact desired entries, user-scope commands, timeout/approval defaults, and
uninstall drift refusal.
