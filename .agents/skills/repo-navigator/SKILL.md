# Repo Navigator

## Purpose
Find the right files without scanning the whole repository.

## Trigger
Use when a task requires understanding where code lives, finding related files, or mapping a feature to modules.

## Workflow
1. Read `AGENTS.md` or `CLAUDE.md`.
2. Read `docs/agent/INDEX.md`.
3. Read `docs/agent/CODEMAP.md`.
4. Select relevant module cards from `docs/agent/module-cards/`.
5. Use `rg` or targeted file reads for discovery.
6. Return file candidates and confidence.

## Output
- Relevant docs read
- Candidate files
- Related tests
- Confidence level
- Suggested next step

## Constraints
- Do not inspect unrelated directories.
- Do not make edits.
- Prefer targeted search over broad reads.
