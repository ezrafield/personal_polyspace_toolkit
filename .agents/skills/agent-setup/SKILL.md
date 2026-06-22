# Agent Setup

## Purpose
Diagnose and configure the Personal Polyspace Toolkit through its deterministic CLI.

## Workflow
1. Run `python -m personal_polyspace_toolkit.cli doctor --json`.
2. Read `skills/toolkit-setup/SKILL.md`.
3. Preview the exact clients and paths with `setup --dry-run`.
4. Obtain confirmation, perform setup, restart the client, and run `verify`.
5. For Qwen Code, follow `docs/setup/qwen-local.md` without modifying settings automatically.

## Constraints
- Never bypass digest verification or ownership conflicts.
- Never enable telemetry implicitly.
- Do not remove operating-system download protections.
- Report missing Polyspace separately from MCP binary or client configuration state.
