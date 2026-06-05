# Tools

Use deterministic scripts for repeatable, cheap, auditable work.

## Included Scripts

| Script | Purpose |
| --- | --- |
| `scripts/generate_codemap.py` | Refresh `docs/agent/CODEMAP.md` from source folders. |
| `scripts/summarize_changed_files.py` | Summarize changed files for handoff and review. |
| `scripts/update_module_cards.py` | Create missing module cards from source folders. |
| `scripts/run_targeted_tests.py` | Run a focused test command or pick a small default. |
| `scripts/validate_agent_docs.py` | Validate required agent docs and skill templates. |
| `scripts/detect_large_context_docs.py` | Warn when auto-loaded docs become too large. |
| `scripts/check_architecture_boundaries.py` | Catch simple layer import violations. |
| `scripts/collect_task_trace.py` | Create a task trace from current changed files. |

## Make Targets

```bash
make docs-map
make update-module-cards
make targeted-tests
make validate-agent-docs
make detect-large-context-docs
make check-architecture-boundaries
make task-trace
```

## Tool Principles

- Prefer scripts for deterministic checks.
- Prefer targeted checks before broad suites.
- Keep scripts safe by default.
- Make script output easy for humans and agents to inspect.
- Avoid hiding policy decisions inside scripts; document decisions in ADRs.
