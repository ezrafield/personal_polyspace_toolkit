---
name: toolkit-setup
description: Safely installs or diagnoses the unofficial Personal Polyspace Toolkit for Codex or Claude Code.
license: MathWorks restricted BSD-3-Clause derivative
---
# Toolkit Setup

Use the deterministic CLI instead of manually downloading binaries or editing client configuration.

1. Run `polyspace-toolkit doctor --json` and report missing prerequisites.
2. Ask which supported automated clients to configure: `codex`, `claude`, or both.
3. Run `polyspace-toolkit setup --client <client> --dry-run` and show the plan.
4. After approval, rerun without `--dry-run`. Do not add `--enable-telemetry` unless requested.
5. Run `polyspace-toolkit verify --client <client>`.

Qwen Code setup is manual. Follow `docs/setup/qwen-local.md`; never edit Qwen settings automatically.

Do not bypass digest verification, remove operating-system download protections, or overwrite an
unknown `polyspace` MCP registration without explicit approval.

Derived from the MathWorks Polyspace Agentic Toolkit setup workflow.
