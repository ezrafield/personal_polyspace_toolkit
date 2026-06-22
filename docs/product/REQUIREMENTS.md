# Requirements

## Functional

- Detect supported hosts and Polyspace R2024b+ without broad searches.
- Install only tested MCP release assets after SHA-256 verification.
- Configure Codex and Claude at user scope while preserving unrelated settings.
- Provide manual, non-secret Qwen local-model and MCP examples.
- Validate a versioned C-only project configuration with explicit profiles.
- Provide analysis, remediation, justification, configuration, documentation, catalog, and PSTUnit
  skills with direct binary fallbacks where applicable.
- Verify and uninstall only state owned by this toolkit.

## Quality

- Python 3.11+, strict typing, no secrets in state or examples.
- Tests on Windows, Linux, and macOS using temporary homes and fake external tools.
- Real Polyspace execution remains opt-in and is required before a stable release claim.
- Active product surfaces must not reference removed clients or unsupported language workflows.
