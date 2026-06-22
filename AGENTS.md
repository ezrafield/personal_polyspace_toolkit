# Personal Polyspace Toolkit Agent Guide

## Purpose
This is an unofficial C-only derivative used with Polyspace as You Code. It owns deterministic
setup, supported-client registration, project configuration validation, and guarded Polyspace skills.

## Required Workflow
1. Read `docs/agent/INDEX.md`.
2. Check `.agent/memory/index.json`, then verify relevant memory against current files.
3. Read only the relevant module card and skill.
4. Use `rg` for exact confirmation; do not scan the whole repository without need.
5. Make the smallest safe change and add tests for behavior changes.
6. Run targeted tests before broad tests.
7. Summarize files, commands, and remaining risks.

## Product Invariants
- C translation units only; headers are analyzed through a containing `.c` file.
- Never select a checker profile implicitly.
- Never auto-justify a finding or run generated test code without explicit approval.
- Keep the five MCP tool names in `src/personal_polyspace_toolkit/constants.py` compatible.
- Qwen setup is documentation-only; do not create a Qwen extension or edit Qwen settings.
- Telemetry remains disabled unless the user explicitly enables it.
- Do not bypass digest checks, ownership conflicts, or operating-system download protections.
- Current source, tests, schemas, and official installed-release documentation override memory.

## Commands
- Install: `python -m pip install -e ".[dev]"`
- Unit tests: `python -m pytest tests/unit -q`
- Integration tests: `python -m pytest tests/integration -q`
- Lint: `python -m ruff check src tests scripts`
- Typecheck: `python -m mypy`
- Agent audits: `make validate-agent-docs`, `make audit-module-cards`, `make audit-memory`
