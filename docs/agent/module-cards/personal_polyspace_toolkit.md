# Module: Personal Polyspace Toolkit

## Responsibility
Implements the public CLI and deterministic setup/configuration behavior.

## Key Files
- `cli.py`: command boundary
- `installer.py`: stateful orchestration
- `clients.py`: supported automated client adapters
- `project_config.py`: public project schema behavior

## Public Interfaces
- `polyspace-toolkit` console command
- `ProjectConfig` and configuration validation
- Tested release manifest and five MCP compatibility names

## Rules
- Keep platform and external-process side effects behind focused modules.
- Preserve unrelated user configuration and refuse drifted ownership.
- Keep Qwen verification read-only.
- Add tests for every public behavior change.
