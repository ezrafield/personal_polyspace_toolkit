# Module: Installer

## Responsibility
Owns platform discovery, supported-release selection, verified binary installation, skill deployment,
state persistence, verification, and uninstall.

## Rules
- All downloads flow through `releases.py`.
- All state writes are atomic and contain no secrets.
- Unknown files are user-owned; collisions require explicit replacement and backup.
- Partial failure must leave the previous usable state intact or report exact manual recovery.

## Tests
Platform/version gates, digest mismatch, rollback, idempotency, collision, and drift tests.
