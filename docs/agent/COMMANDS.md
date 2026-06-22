# Commands

| Task | Command |
| --- | --- |
| Install development environment | `python -m pip install -e ".[dev]"` |
| Inspect prerequisites | `polyspace-toolkit doctor --json` |
| Preview setup | `polyspace-toolkit setup --client codex --dry-run` |
| Validate project config | `polyspace-toolkit config validate .polyspace-toolkit.json` |
| Unit tests | `python -m pytest tests/unit -q` |
| Integration tests | `python -m pytest tests/integration -q` |
| Lint | `python -m ruff check src tests scripts` |
| Typecheck | `python -m mypy` |
| Agent docs | `python scripts/validate_agent_docs.py` |

No normal development command requires a licensed Polyspace installation. The smoke target does.
