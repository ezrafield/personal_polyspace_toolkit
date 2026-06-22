# Architecture

The product has three layers:

1. **Deterministic Python core**: discovers installations, validates versions and project config,
   downloads verified MCP assets, manages ownership state, and configures supported clients.
2. **Canonical skills**: progressive Polyspace domain workflows under `skills/`; these call the
   existing MCP tools or documented direct binary fallbacks.
3. **Client surfaces**: Codex and Claude metadata plus manual Qwen Code documentation.

## Boundaries

- `cli.py` parses user intent and formats results; it delegates behavior.
- `installer.py` orchestrates stateful operations through discovery, release, state, and client APIs.
- `clients.py` owns client-specific configuration and must preserve unrelated user settings.
- `releases.py` is the only network download boundary.
- `project_config.py` validates project data without mutating it.
- Skills do not implement installers and Python code does not encode finding-remediation prompts.

## Safety Invariants

- Setup is plan-first and confirmation-gated unless `--yes` is explicit.
- Release versions and digests come from the tested manifest.
- Unknown existing configuration is user-owned.
- State never stores secrets.
- C checker profiles are explicit and C source filtering is enforced independently of agent behavior.
