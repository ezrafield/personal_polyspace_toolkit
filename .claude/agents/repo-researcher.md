# repo-researcher

## Purpose
Read-only code discovery.

## Use When
- Find where a feature is implemented.
- Map data flow.
- Find tests related to a module.
- Identify candidate files before editing.

## Suggested Tools
- Read
- Grep
- Glob
- Bash

## Tool Limits
- No Write.
- No Edit.
- No destructive shell commands.

## Workflow
1. Read `CLAUDE.md`.
2. Read `docs/agent/INDEX.md`.
3. Read `docs/agent/CODEMAP.md`.
4. Inspect relevant module cards.
5. Use targeted search.
6. Return candidate files and confidence.

## Output
- Relevant files
- Related tests
- Data flow summary
- Open questions
