# Agent Setup

## Purpose
Bootstrap this agent kit inside a real project without replacing project-specific context.

## Trigger
Use after installing the kit in a project, when project stack context is missing, or when `docs/agent/CODEMAP.md` and module cards need to be initialized.

## Workflow
1. Run `python scripts/agent_setup.py`.
2. Review detected stack and commands in `docs/agent/COMMANDS.md`.
3. Fill TODOs in generated `docs/agent/CODEMAP.md` and module cards with real architecture notes.
4. Create or update project-specific `AGENTS.md` and `CLAUDE.md` only when needed.
5. Run validation:
   - `python scripts/validate_agent_docs.py`
   - `python scripts/check_context_staleness.py`
   - `python scripts/audit_module_cards.py`
   - `python scripts/detect_large_agent_files.py`

## Output
- Detected stack
- Detected test, lint, typecheck, and dev commands
- Generated or updated agent docs
- Validation results
- Remaining TODOs

## Constraints
- Preserve existing project instructions.
- Do not overwrite user-owned `AGENTS.md` or `CLAUDE.md` content.
- Keep generated context concise.
- Prefer deterministic scripts over broad manual repository scans.
